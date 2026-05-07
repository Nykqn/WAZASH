from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.correlation.schemas import CorrelationGroup
from app.models.correlation import CorrelationGroup as CorrelationGroupModel
from app.models.user import User

router = APIRouter(tags=["correlation"])


@router.get("/correlations", response_model=list[CorrelationGroup])
async def list_correlations(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
    format: str = "json",
    limit: int = 100,
    offset: int = 0,
):
    groups = db.query(CorrelationGroupModel).order_by(CorrelationGroupModel.created_at.desc()).offset(offset).limit(limit).all()

    if format == "csv":
        header = "id,correlation_type,source_ip,target_ip,event_type,event_count,window_start,window_end,created_at\n"
        rows = ""
        for g in groups:
            rows += f"{g.id},{g.correlation_type},{g.source_ip},{g.target_ip or ''},{g.event_type or ''},{g.event_count},{g.window_start},{g.window_end},{g.created_at}\n"
        return Response(content=header + rows, media_type="text/csv")

    return groups
