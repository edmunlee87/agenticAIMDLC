"""Session manager.

:class:`SessionManager` tracks active and historical UI/agent sessions per
run.  Sessions are created, suspended, resumed, and closed as actors move
through the workflow.  Each session record is immutable; updates produce new
instances via ``model_copy``.

Design contract:
    - Returns plain Python values or raises on error.
    - The :class:`~sdk.workflowsdk.service.WorkflowService` wraps results in
      :class:`~sdk.platform_core.schemas.base_result.BaseResult`.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

from sdk.platform_core.schemas.utilities import IDFactory, TimeProvider
from sdk.workflowsdk.models import (
    SessionRecord,
    SessionStatus,
    UIMode,
)

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages :class:`SessionRecord` objects for a single run.

    Sessions are identified by ``session_id``; only one session should be
    ``ACTIVE`` at a time (enforced by :meth:`create`).
    """

    def __init__(self) -> None:
        # session_id -> SessionRecord
        self._by_id: Dict[str, SessionRecord] = {}
        # run_id -> list of session_ids in creation order
        self._by_run: Dict[str, List[str]] = {}

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def create(
        self,
        *,
        run_id: str,
        project_id: str,
        created_by: str = "",
        ui_mode: UIMode = UIMode.IDLE,
        last_stage: str = "",
        checkpoint_id: str = "",
        metadata: Optional[Dict] = None,
    ) -> SessionRecord:
        """Create a new session for *run_id*.

        Any currently ``ACTIVE`` session for the same run is automatically
        suspended before the new session is created.

        Args:
            run_id: Associated run identifier.
            project_id: Owning project identifier.
            created_by: Actor creating the session.
            ui_mode: Initial UI mode.
            last_stage: Stage active when the session starts.
            checkpoint_id: Starting checkpoint ID (if resuming from one).
            metadata: Arbitrary session metadata.

        Returns:
            Newly created :class:`SessionRecord`.

        Raises:
            ValueError: If *run_id* or *project_id* is empty.
        """
        if not run_id.strip():
            raise ValueError("run_id must be non-empty.")
        if not project_id.strip():
            raise ValueError("project_id must be non-empty.")

        # Suspend any active session for this run
        for sid in self._by_run.get(run_id, []):
            existing = self._by_id.get(sid)
            if existing and existing.status == SessionStatus.ACTIVE:
                self._by_id[sid] = existing.model_copy(
                    update={"status": SessionStatus.SUSPENDED}
                )
                logger.debug(
                    "Session suspended (new session creating): sid=%s run=%s",
                    sid,
                    run_id,
                )

        now = TimeProvider.now()
        session_id = IDFactory.session_id()
        session = SessionRecord(
            session_id=session_id,
            run_id=run_id,
            project_id=project_id,
            created_by=created_by,
            created_at=now,
            last_active_at=now,
            status=SessionStatus.ACTIVE,
            ui_mode=ui_mode,
            last_stage=last_stage,
            checkpoint_id=checkpoint_id,
            metadata=metadata or {},
        )
        self._by_id[session_id] = session
        self._by_run.setdefault(run_id, []).append(session_id)

        logger.debug(
            "Session created: sid=%s run=%s actor=%s",
            session_id,
            run_id,
            created_by,
        )
        return session

    def update_activity(
        self,
        session_id: str,
        *,
        ui_mode: Optional[UIMode] = None,
        last_stage: Optional[str] = None,
        checkpoint_id: Optional[str] = None,
    ) -> SessionRecord:
        """Refresh the ``last_active_at`` timestamp and optional fields.

        Args:
            session_id: Session to update.
            ui_mode: New UI mode (if changed).
            last_stage: New last stage (if changed).
            checkpoint_id: New checkpoint ID (if changed).

        Returns:
            Updated :class:`SessionRecord`.

        Raises:
            KeyError: If *session_id* is not found.
            ValueError: If the session is not ``ACTIVE``.
        """
        session = self._get_or_raise(session_id)
        if session.status != SessionStatus.ACTIVE:
            raise ValueError(
                f"Session '{session_id}' is not ACTIVE "
                f"(current: {session.status.value})."
            )
        updates: Dict = {"last_active_at": TimeProvider.now()}
        if ui_mode is not None:
            updates["ui_mode"] = ui_mode
        if last_stage is not None:
            updates["last_stage"] = last_stage
        if checkpoint_id is not None:
            updates["checkpoint_id"] = checkpoint_id

        updated = session.model_copy(update=updates)
        self._by_id[session_id] = updated
        return updated

    def suspend(self, session_id: str) -> SessionRecord:
        """Suspend an active session.

        Args:
            session_id: Session to suspend.

        Returns:
            Updated :class:`SessionRecord`.

        Raises:
            KeyError: If not found.
            ValueError: If the session is not ``ACTIVE``.
        """
        session = self._get_or_raise(session_id)
        if session.status != SessionStatus.ACTIVE:
            raise ValueError(
                f"Session '{session_id}' cannot be suspended "
                f"(current: {session.status.value})."
            )
        updated = session.model_copy(update={"status": SessionStatus.SUSPENDED})
        self._by_id[session_id] = updated
        logger.debug("Session suspended: sid=%s", session_id)
        return updated

    def resume(self, session_id: str) -> SessionRecord:
        """Resume a suspended session.

        Args:
            session_id: Session to resume.

        Returns:
            Updated :class:`SessionRecord`.

        Raises:
            KeyError: If not found.
            ValueError: If the session is not ``SUSPENDED``.
        """
        session = self._get_or_raise(session_id)
        if session.status != SessionStatus.SUSPENDED:
            raise ValueError(
                f"Session '{session_id}' cannot be resumed "
                f"(current: {session.status.value})."
            )
        updated = session.model_copy(
            update={
                "status": SessionStatus.ACTIVE,
                "last_active_at": TimeProvider.now(),
            }
        )
        self._by_id[session_id] = updated
        logger.debug("Session resumed: sid=%s", session_id)
        return updated

    def close(self, session_id: str) -> SessionRecord:
        """Close a session permanently.

        Args:
            session_id: Session to close.

        Returns:
            Updated :class:`SessionRecord`.

        Raises:
            KeyError: If not found.
            ValueError: If already closed.
        """
        session = self._get_or_raise(session_id)
        if session.status == SessionStatus.CLOSED:
            raise ValueError(f"Session '{session_id}' is already closed.")
        updated = session.model_copy(
            update={
                "status": SessionStatus.CLOSED,
                "closed_at": TimeProvider.now(),
            }
        )
        self._by_id[session_id] = updated
        logger.debug("Session closed: sid=%s", session_id)
        return updated

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get(self, session_id: str) -> SessionRecord:
        """Return a :class:`SessionRecord` by ID.

        Args:
            session_id: Target session.

        Returns:
            Matching :class:`SessionRecord`.

        Raises:
            KeyError: If not found.
        """
        return self._get_or_raise(session_id)

    def active_for_run(self, run_id: str) -> Optional[SessionRecord]:
        """Return the active session for *run_id*, or ``None``.

        Args:
            run_id: Run to query.

        Returns:
            Active :class:`SessionRecord` or ``None``.
        """
        for sid in reversed(self._by_run.get(run_id, [])):
            session = self._by_id.get(sid)
            if session and session.status == SessionStatus.ACTIVE:
                return session
        return None

    def list_for_run(self, run_id: str) -> List[SessionRecord]:
        """Return all sessions for *run_id* in chronological order.

        Args:
            run_id: Run to query.

        Returns:
            Ordered list of :class:`SessionRecord` objects.
        """
        sids = self._by_run.get(run_id, [])
        return [self._by_id[sid] for sid in sids if sid in self._by_id]

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_or_raise(self, session_id: str) -> SessionRecord:
        session = self._by_id.get(session_id)
        if session is None:
            raise KeyError(f"Session '{session_id}' not found.")
        return session
