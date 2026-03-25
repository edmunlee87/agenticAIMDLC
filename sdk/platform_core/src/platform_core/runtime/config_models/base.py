"""Base Pydantic model for all runtime config fragments.

All config models extend :class:`ConfigModelBase` which enforces immutability
and strict validation. Config models never have audit/governance payload fields
(those live in payload schemas). They define *what the system is allowed to do*,
not *what happened*.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ConfigModelBase(BaseModel):
    """Root for all MDLC runtime config Pydantic models.

    Characteristics:
    - ``frozen=True``: immutable after construction; pass new instances to update.
    - ``extra="forbid"``: any unknown key in YAML/dict raises a validation error.
    - ``populate_by_name=True``: allows both alias and field name during deserialization.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        populate_by_name=True,
    )
