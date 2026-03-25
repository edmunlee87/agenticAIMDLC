"""Base Pydantic model for all runtime config models.

Enforces strict validation: no extra fields, assignment validation enabled,
and enum values coerced to their underlying types.
"""

from pydantic import BaseModel, ConfigDict


class RuntimeConfigBase(BaseModel):
    """Root base for all Pydantic runtime config models.

    Enforces:
    - extra = "forbid": unknown fields raise a validation error.
    - validate_assignment = True: field re-assignment is validated.
    - use_enum_values = True: enum fields store the raw value, not the enum member.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True,
        str_strip_whitespace=True,
    )
