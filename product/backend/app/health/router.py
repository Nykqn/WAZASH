"""Router pour le health check."""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check() -> dict[str, str]:
    """Vérifie que l'API est opérationnelle."""
    return {"status": "ok", "service": "wazash-backend"}
