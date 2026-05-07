"""Router pour l'ingestion de heartbeats."""

from datetime import datetime as _dt

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, verify_agent_key
from app.core.storage import add_heartbeat, get_heartbeats, seed_default_users
from app.models.user import User
from app.heartbeat.schemas import HeartbeatPayload
from app.models.heartbeat import Heartbeat


def auto_register_asset(db: Session, endpoint_id: str) -> None:
    from app.models.asset import Asset
    existing = db.query(Asset).filter(Asset.endpoint_id == endpoint_id).first()
    if not existing:
        asset = Asset(endpoint_id=endpoint_id, status="active")
        db.add(asset)
        db.commit()


router = APIRouter(tags=["heartbeat"])


@router.post("/heartbeat")
async def receive_heartbeat(payload: HeartbeatPayload, db: Session = Depends(get_db), _: bool = Depends(verify_agent_key)) -> dict[str, str]:
    seed_default_users(db)
    auto_register_asset(db, payload.endpoint_id)
    add_heartbeat(db, payload.model_dump())

    # Update asset last_seen and status
    from app.models.asset import Asset
    asset = db.query(Asset).filter(Asset.endpoint_id == payload.endpoint_id).first()
    if asset:
        asset.last_seen = _dt.utcnow()
        asset.status = payload.status
        db.commit()

    return {"status": "ok"}


@router.get("/heartbeats")
async def list_heartbeats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
    format: str = "json",
    endpoint_id: str | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
):
    """Retourne la liste des heartbeats avec filtres optionnels."""
    seed_default_users(db)
    query = db.query(Heartbeat)
    if endpoint_id:
        query = query.filter(Heartbeat.endpoint_id == endpoint_id)
    if status:
        query = query.filter(Heartbeat.status == status)
    heartbeats = query.order_by(Heartbeat.timestamp.desc()).offset(offset).limit(limit).all()

    if format == "csv":
        header = "id,endpoint_id,timestamp,status,created_at\n"
        rows = ""
        for hb in heartbeats:
            rows += f"{hb.id},{hb.endpoint_id},{hb.timestamp},{hb.status},{hb.created_at}\n"
        return Response(content=header + rows, media_type="text/csv")

    return heartbeats
