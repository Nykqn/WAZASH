"""Router pour la gestion des logs d'audit."""

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.storage import get_audit_logs, seed_default_users

router = APIRouter(tags=["audit"])


@router.get("/")
async def list_audit_logs(
    db: Session = Depends(get_db),
    format: str = "json",
    action: str | None = None,
    user_email: str | None = None,
):
    """Retourne la liste des logs d'audit avec filtres optionnels."""
    seed_default_users(db)
    from app.models.audit import AuditLog
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    if user_email:
        query = query.filter(AuditLog.user_email == user_email)
    logs = query.order_by(AuditLog.timestamp.desc()).all()

    if format == "csv":
        header = "id,timestamp,action,user_email,details,created_at\n"
        rows = ""
        for log in logs:
            details = log.details.replace(",", ";").replace("\n", " ")
            rows += f"{log.id},{log.timestamp},{log.action},{log.user_email},{details},{log.created_at}\n"
        return Response(content=header + rows, media_type="text/csv")

    return logs
