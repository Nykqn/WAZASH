"""Point d'entrée de l'application FastAPI."""

from fastapi import FastAPI

from app.core.config import settings
from app.health.router import router as health_router
from app.auth.router import router as auth_router
from app.heartbeat.router import router as heartbeat_router
from app.events.router import router as events_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(health_router)
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(heartbeat_router, prefix=settings.api_v1_prefix)
app.include_router(events_router, prefix=settings.api_v1_prefix)
