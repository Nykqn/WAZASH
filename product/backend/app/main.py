"""Point d'entrée de l'application FastAPI."""

from fastapi import FastAPI

from app.core.config import settings
from app.health.router import router as health_router
from app.auth.router import router as auth_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(health_router)
app.include_router(auth_router)
