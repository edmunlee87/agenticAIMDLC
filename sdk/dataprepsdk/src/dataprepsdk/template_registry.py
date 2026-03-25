"""dataprepsdk.template_registry -- versioned registry for DataPrepTemplates."""

from __future__ import annotations

import logging

from dataprepsdk.models import DataPrepTemplate, TemplateType

logger = logging.getLogger(__name__)


class TemplateRegistry:
    """Registry for :class:`~dataprepsdk.models.DataPrepTemplate` objects.

    Supports multiple versions of the same template; the latest version is
    returned by default.
    """

    def __init__(self) -> None:
        # template_id -> list of versions (ordered oldest→newest)
        self._templates: dict[str, list[DataPrepTemplate]] = {}

    def register(self, template: DataPrepTemplate) -> None:
        """Register a new template version.

        Args:
            template: :class:`DataPrepTemplate` to register.
        """
        versions = self._templates.setdefault(template.template_id, [])
        # Prevent duplicate version registration.
        if any(t.version == template.version for t in versions):
            raise ValueError(
                f"Template '{template.template_id}' version '{template.version}' already registered."
            )
        versions.append(template)
        logger.info(
            "template_registry.registered",
            extra={"template_id": template.template_id, "version": template.version},
        )

    def get(self, template_id: str, version: str | None = None) -> DataPrepTemplate:
        """Retrieve a template by ID and optional version.

        Args:
            template_id: Template identifier.
            version: Version string. If None, returns the latest registered version.

        Returns:
            :class:`DataPrepTemplate`.

        Raises:
            KeyError: If template_id not found.
            KeyError: If the requested version is not registered.
        """
        versions = self._templates.get(template_id)
        if not versions:
            raise KeyError(f"Template '{template_id}' not found in registry.")
        if version is None:
            return versions[-1]  # latest
        matches = [t for t in versions if t.version == version]
        if not matches:
            raise KeyError(f"Template '{template_id}' version '{version}' not found.")
        return matches[0]

    def list_all(self) -> list[DataPrepTemplate]:
        """Return all registered templates (latest version of each).

        Returns:
            List of :class:`DataPrepTemplate`.
        """
        return [versions[-1] for versions in self._templates.values()]

    def list_by_type(self, template_type: TemplateType) -> list[DataPrepTemplate]:
        """Return all templates of a specific type (latest version).

        Args:
            template_type: :class:`TemplateType` to filter by.

        Returns:
            List of :class:`DataPrepTemplate`.
        """
        return [t for t in self.list_all() if t.template_type == template_type]

    def list_versions(self, template_id: str) -> list[str]:
        """Return all registered versions for a template.

        Args:
            template_id: Template identifier.

        Returns:
            List of version strings (oldest first).
        """
        versions = self._templates.get(template_id, [])
        return [t.version for t in versions]
