from fastapi import APIRouter

from backend.app.schemas.query import (
    ExplainResponse,
    QueryRequest,
    QueryResponse,
)
from backend.app.services.query import QueryService


router = APIRouter(
    prefix="/api/query",
    tags=["query"],
)


@router.post(
    "/execute",
    response_model=QueryResponse,
)
def execute_query(
    request: QueryRequest,
) -> QueryResponse:
    service = QueryService()

    result = service.execute_query(request.query)

    return QueryResponse(**result)


@router.post(
    "/explain",
    response_model=ExplainResponse,
)
def explain_query(
    request: QueryRequest,
) -> ExplainResponse:
    service = QueryService()

    result = service.explain_query(request.query)

    return ExplainResponse(**result)