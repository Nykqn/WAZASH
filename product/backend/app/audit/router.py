"""Router pour la gestion des logs d'audit."""

from datetime import datetime

from fastapi import APIRouter

from app.audit.schemas import AuditLog
from app.core.storage import get_audit_logs

router = APIRouter(tags=["audit"])


@router.get("/")
async def list_audit_logs() -> list[AuditLog]:
    """Retourne la liste des logs d'audit par ordre chronologique inversé."""
    logs = get_audit_logs()
    return sorted(logs, key=lambda x: x.timestamp, reverse=True)
