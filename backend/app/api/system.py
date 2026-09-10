from fastapi import APIRouter

from backend.app.schemas.system import SystemHealthResponse
from backend.app.services.system import SystemHealthService


router = APIRouter(
    prefix="/api/system",
    tags=["system"],
)


@router.get(
    "/health",
    response_model=SystemHealthResponse,
)
def get_system_health() -> SystemHealthResponse:
    service = SystemHealthService()

    return service.get_health()