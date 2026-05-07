from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.core.storage import add_audit_log, seed_default_users
from app.assets.schemas import Asset as AssetSchema, AssetCreate, AssetUpdate
from app.models.asset import Asset
from app.models.user import User

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("/", response_model=list[AssetSchema])
async def list_assets(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
    format: str = "json",
    status_filter: str | None = None,
):
    seed_default_users(db)
    query = db.query(Asset)
    if status_filter:
        query = query.filter(Asset.status == status_filter)
    assets = query.order_by(Asset.updated_at.desc()).all()

    if format == "csv":
        header = "id,endpoint_id,hostname,ip_address,os,status,last_seen,created_at\n"
        rows = ""
        for a in assets:
            rows += f"{a.id},{a.endpoint_id},{a.hostname or ''},{a.ip_address or ''},{a.os or ''},{a.status},{a.last_seen or ''},{a.created_at}\n"
        return Response(content=header + rows, media_type="text/csv")

    return assets


@router.post("/", response_model=AssetSchema, status_code=status.HTTP_201_CREATED)
async def create_asset(payload: AssetCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    seed_default_users(db)
    existing = db.query(Asset).filter(Asset.endpoint_id == payload.endpoint_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Asset already exists")

    asset = Asset(
        endpoint_id=payload.endpoint_id,
        hostname=payload.hostname,
        ip_address=payload.ip_address,
        os=payload.os,
        status="active",
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    add_audit_log(db, "asset_created", None, f"Asset {asset.endpoint_id} créé")
    return asset


@router.get("/{endpoint_id}", response_model=AssetSchema)
async def get_asset(endpoint_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    seed_default_users(db)
    asset = db.query(Asset).filter(Asset.endpoint_id == endpoint_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.patch("/{endpoint_id}", response_model=AssetSchema)
async def update_asset(endpoint_id: str, payload: AssetUpdate, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    seed_default_users(db)
    asset = db.query(Asset).filter(Asset.endpoint_id == endpoint_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(asset, key, value)

    db.commit()
    db.refresh(asset)
    add_audit_log(db, "asset_updated", None, f"Asset {endpoint_id} modifié")
    return asset


@router.delete("/{endpoint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(endpoint_id: str, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    seed_default_users(db)
    asset = db.query(Asset).filter(Asset.endpoint_id == endpoint_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    db.delete(asset)
    db.commit()
    add_audit_log(db, "asset_deleted", None, f"Asset {endpoint_id} supprimé")
