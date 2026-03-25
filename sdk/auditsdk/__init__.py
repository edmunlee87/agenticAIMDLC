"""Audit SDK.

Provides AuditService for writing immutable, append-only audit records,
registering decisions/approvals/exceptions, and exporting audit bundles.
"""

from sdk.auditsdk.audit_service import AuditService
from sdk.auditsdk.models import AUDIT_TYPES, AuditBundle, AuditRecord

__version__ = "0.1.0"

__all__ = [
    "AuditService",
    "AuditRecord",
    "AuditBundle",
    "AUDIT_TYPES",
]
