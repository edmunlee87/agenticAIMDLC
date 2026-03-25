"""BaseModelBase: root for all typed domain models in the platform.

Every schema-bound model (payloads, fragments, results) inherits from this class
to gain standardized serialization and immutable-copy helpers.
"""

import json
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class BaseModelBase(BaseModel):
    """Root base for all typed platform domain models.

    Provides:
    - to_dict: Full dict representation.
    - compact_dict: Dict with None values removed.
    - to_json: JSON string representation.
    - with_updates: Immutable copy with field updates applied.

    Design rules:
    - Shallow inheritance preferred; prefer composition for complex structures.
    - extra = "ignore" to allow future fields without breaking existing consumers.
    - validate_assignment enabled for runtime safety.
    """

    model_config = ConfigDict(
        extra="ignore",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    def to_dict(self) -> Dict[str, Any]:
        """Return a full dict representation of this model.

        Returns:
            Dict with all fields, including None values.
        """
        return self.model_dump(mode="python")

    def compact_dict(self) -> Dict[str, Any]:
        """Return a dict with None and empty-collection fields excluded.

        Returns:
            Dict with only non-None, non-empty fields.
        """
        return self.model_dump(mode="python", exclude_none=True)

    def to_json(self, indent: Optional[int] = None) -> str:
        """Return a JSON string representation.

        Args:
            indent: JSON indent width. None for compact output.

        Returns:
            JSON-serialized string.
        """
        return self.model_dump_json(indent=indent)

    def with_updates(self, **kwargs: Any) -> "BaseModelBase":
        """Return an immutable copy with the given field updates applied.

        Args:
            **kwargs: Field name to new value mappings.

        Returns:
            New instance with updates applied.

        Raises:
            ValidationError: If any updated field value fails validation.
        """
        return self.model_copy(update=kwargs)
