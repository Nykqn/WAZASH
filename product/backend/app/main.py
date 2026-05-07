"""Point d'entrée de l'application FastAPI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.health.router import router as health_router
from app.auth.router import router as auth_router
from app.heartbeat.router import router as heartbeat_router
from app.events.router import router as events_router
from app.alerts.router import router as alerts_router
from app.audit.router import router as audit_router
from app.assets.router import router as assets_router
from app.correlation.router import router as correlation_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(heartbeat_router, prefix=settings.api_v1_prefix)
app.include_router(events_router, prefix=settings.api_v1_prefix)
app.include_router(alerts_router, prefix=f"{settings.api_v1_prefix}/alerts")
app.include_router(audit_router, prefix=f"{settings.api_v1_prefix}/audit")
app.include_router(assets_router, prefix=settings.api_v1_prefix)
app.include_router(correlation_router, prefix=settings.api_v1_prefix)
