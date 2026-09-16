from fastapi import APIRouter, HTTPException

from backend.app.schemas.analytics import (
    AnalyticsRequest,
    AnalyticsResponse,
)
from backend.app.services.analytics import AnalyticsService


router = APIRouter(
    prefix="/api/analytics",
    tags=["analytics"],
)


@router.post(
    "/query",
    response_model=AnalyticsResponse,
)
def execute_analytics(
    request: AnalyticsRequest,
) -> AnalyticsResponse:
    service = AnalyticsService()

    try:
        return service.execute(request)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc