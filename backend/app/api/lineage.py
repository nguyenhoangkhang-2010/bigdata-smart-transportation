from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.lineage import (
    LineageResponse,
)
from backend.app.services.lineage import LineageService


router = APIRouter(
    prefix="/api/lineage",
    tags=["lineage"],
)


@router.get(
    "",
    response_model=list[LineageResponse],
)
def get_lineage(
    db: Session = Depends(get_db),
) -> list[LineageResponse]:
    service = LineageService(db)

    return service.get_lineage()


@router.get(
    "/{pipeline_name}",
    response_model=LineageResponse,
)
def get_pipeline_lineage(
    pipeline_name: str,
    db: Session = Depends(get_db),
) -> LineageResponse:
    service = LineageService(db)

    result = service.get_pipeline_lineage(pipeline_name)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pipeline '{pipeline_name}' not found.",
        )

    return result