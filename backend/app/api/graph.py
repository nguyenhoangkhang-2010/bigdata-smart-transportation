from fastapi import APIRouter, HTTPException

from backend.app.schemas.graph import (
    GraphQueryRequest,
    GraphResponse,
)
from backend.app.services.graph import GraphService


router = APIRouter(
    prefix="/api/graph",
    tags=["graph"],
)


@router.post(
    "/query",
    response_model=GraphResponse,
)
def query_graph(
    request: GraphQueryRequest,
) -> GraphResponse:
    service = GraphService()

    try:
        result = service.query_graph(
            table=request.table,
            source_column=request.source_column,
            target_column=request.target_column,
            relationship_column=request.relationship_column,
            node_label_column=request.node_label_column,
        )

        return GraphResponse(**result)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc