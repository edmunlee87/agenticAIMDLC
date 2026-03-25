"""Jupyter display utilities for MDLC workflow UX.

Provides helper functions that render MDLC SDK objects as rich IPython display
objects inside Jupyter / JupyterLab.  Falls back to plain text if IPython is
not available (useful for unit tests).

Supported renders:
- :func:`show_workflow_state` -- current workflow state summary table.
- :func:`show_review_payload` -- 3-panel review card.
- :func:`show_response_envelope` -- governance-aware response summary.
- :func:`show_policy_findings` -- policy evaluation findings grid.
"""

from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

_IPYTHON_AVAILABLE = False
try:
    from IPython.display import HTML, display  # type: ignore[import]
    _IPYTHON_AVAILABLE = True
except ImportError:
    pass


def _render_or_print(html: str, plain: str) -> None:
    if _IPYTHON_AVAILABLE:
        display(HTML(html))  # type: ignore[name-defined]
    else:
        print(plain)


def show_workflow_state(state: Any) -> None:
    """Render a :class:`~workflowsdk.models.WorkflowState` as an HTML status card.

    Args:
        state: :class:`~workflowsdk.models.WorkflowState` instance.
    """
    if state is None:
        _render_or_print("<em>No workflow state found.</em>", "No workflow state found.")
        return

    current = getattr(state, "current_stage", "—")
    status = getattr(state, "status", "—")
    run_id = getattr(state, "run_id", "—")
    blocked = getattr(state, "is_blocked", False)
    block_color = "orange" if blocked else "green"

    rows = f"""
        <tr><td><b>run_id</b></td><td>{run_id}</td></tr>
        <tr><td><b>current_stage</b></td><td>{current}</td></tr>
        <tr><td><b>status</b></td><td style='color:{block_color}'>{status}</td></tr>
        <tr><td><b>is_blocked</b></td><td>{blocked}</td></tr>
    """
    html = f"<table border='1' style='border-collapse:collapse;font-family:monospace'>{rows}</table>"
    plain = f"run_id={run_id}  stage={current}  status={status}  blocked={blocked}"
    _render_or_print(html, plain)


def show_review_payload(review_payload: Any) -> None:
    """Render a review payload dict as a 3-panel HTML card.

    Args:
        review_payload: Dict returned by :func:`~hitlsdk.service.HITLService.build_review_payload`.
    """
    if review_payload is None:
        _render_or_print("<em>No review payload.</em>", "No review payload.")
        return

    evidence = review_payload.get("evidence_refs", [])
    summary = review_payload.get("summary_for_reviewer", "")
    review_id = review_payload.get("review_id", "—")
    stage = review_payload.get("stage_name", "—")

    evidence_html = "<br/>".join(str(e) for e in evidence) or "<em>none</em>"
    html = f"""
        <div style="display:flex;gap:16px;font-family:monospace">
            <div style="flex:1;border:1px solid #ccc;padding:8px">
                <b>Panel 1 — Context</b><br/>stage: {stage}<br/>review_id: {review_id}
            </div>
            <div style="flex:1;border:1px solid #ccc;padding:8px">
                <b>Panel 2 — Evidence</b><br/>{evidence_html}
            </div>
            <div style="flex:1;border:1px solid #ccc;padding:8px">
                <b>Panel 3 — Summary</b><br/>{summary or '<em>n/a</em>'}
            </div>
        </div>
    """
    plain = f"review_id={review_id}  stage={stage}  summary={summary}"
    _render_or_print(html, plain)


def show_response_envelope(envelope: Any) -> None:
    """Render a :class:`~platform_core.schemas.payloads.StandardResponseEnvelope`.

    Args:
        envelope: :class:`StandardResponseEnvelope` instance or dict.
    """
    if envelope is None:
        _render_or_print("<em>No response.</em>", "No response.")
        return

    if hasattr(envelope, "model_dump"):
        d = envelope.model_dump()
    elif isinstance(envelope, dict):
        d = envelope
    else:
        d = {}

    status = d.get("status", "—")
    color = "green" if status == "ok" else "red"
    run_id = d.get("run_id", "—")
    stage = d.get("stage_name", "—")
    message = d.get("message", "")
    errors = d.get("errors", [])

    error_rows = "".join(
        f"<tr><td>{e.get('code', '')}</td><td>{e.get('message', '')}</td></tr>"
        for e in errors
    )
    error_table = f"<table>{error_rows}</table>" if errors else ""

    html = f"""
        <div style='font-family:monospace;border:1px solid {color};padding:8px'>
            <b style='color:{color}'>status: {status}</b><br/>
            run_id: {run_id}  |  stage: {stage}<br/>
            {message}<br/>
            {error_table}
        </div>
    """
    plain = f"status={status}  run_id={run_id}  stage={stage}  msg={message}"
    if errors:
        plain += f"  errors={json.dumps(errors)}"
    _render_or_print(html, plain)


def show_policy_findings(findings: list[Any]) -> None:
    """Render a list of policy findings as an HTML grid.

    Args:
        findings: List of :class:`~policysdk.models.PolicyFinding` instances or dicts.
    """
    if not findings:
        _render_or_print("<em>No policy findings.</em>", "No policy findings.")
        return

    rows = ""
    for f in findings:
        if hasattr(f, "model_dump"):
            d = f.model_dump()
        elif isinstance(f, dict):
            d = f
        else:
            continue
        sev = d.get("severity", "")
        sev_color = {"critical": "red", "high": "orange", "medium": "yellow", "low": "gray"}.get(
            sev, "black"
        )
        rows += (
            f"<tr>"
            f"<td>{d.get('rule_id', '')}</td>"
            f"<td style='color:{sev_color}'>{sev}</td>"
            f"<td>{d.get('result', '')}</td>"
            f"<td>{d.get('message', '')}</td>"
            f"</tr>"
        )

    html = f"""
        <table border='1' style='border-collapse:collapse;font-family:monospace'>
            <thead><tr><th>rule_id</th><th>severity</th><th>result</th><th>message</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    """
    plain = "\n".join(
        f"[{getattr(f, 'severity', '')}] {getattr(f, 'rule_id', '')} -- {getattr(f, 'result', '')}"
        if hasattr(f, "severity")
        else str(f)
        for f in findings
    )
    _render_or_print(html, plain)
