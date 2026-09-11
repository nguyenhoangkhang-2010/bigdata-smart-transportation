from fastapi import APIRouter, HTTPException

from backend.app.schemas.ingestion import (
    IngestionRequest,
    IngestionResponse,
)
from backend.app.services.ingestion import IngestionService


router = APIRouter(
    prefix="/api/ingestion",
    tags=["ingestion"],
)


@router.post(
    "/events",
    response_model=IngestionResponse,
)
def publish_event(
    request: IngestionRequest,
) -> IngestionResponse:
    try:
        service = IngestionService()

        result = service.publish_pipeline_event(
            event_type=request.event_type,
            pipeline_name=request.pipeline_name,
            payload=request.payload,
        )

        return IngestionResponse(**result)

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to publish ingestion event: {exc}",
        ) from exc