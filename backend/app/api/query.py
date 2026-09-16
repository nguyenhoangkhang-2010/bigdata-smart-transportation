from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.schemas.query import (
    ExplainResponse,
    QueryHistoryResponse,
    QueryRequest,
    QueryResponse,
    SavedQueryCreateRequest,
    SavedQueryResponse,
    SavedQueryUpdateRequest,
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
    db: Session = Depends(get_db),
) -> QueryResponse:
    service = QueryService(db)

    result = service.execute_query(request.query)

    return QueryResponse(**result)


@router.post(
    "/explain",
    response_model=ExplainResponse,
)
def explain_query(
    request: QueryRequest,
    db: Session = Depends(get_db),
) -> ExplainResponse:
    service = QueryService(db)

    result = service.explain_query(request.query)

    return ExplainResponse(**result)


@router.get(
    "/history",
    response_model=list[QueryHistoryResponse],
)
def get_query_history(
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    db: Session = Depends(get_db),
) -> list[QueryHistoryResponse]:
    service = QueryService(db)

    history = service.get_history(
        limit=limit,
        offset=offset,
    )

    return [
        QueryHistoryResponse.model_validate(
            item,
            from_attributes=True,
        )
        for item in history
    ]


@router.post(
    "/saved",
    response_model=SavedQueryResponse,
)
def create_saved_query(
    request: SavedQueryCreateRequest,
    db: Session = Depends(get_db),
) -> SavedQueryResponse:
    service = QueryService(db)

    saved_query = service.create_saved_query(
        name=request.name,
        query=request.query,
        description=request.description,
    )

    return SavedQueryResponse.model_validate(
        saved_query,
        from_attributes=True,
    )


@router.get(
    "/saved",
    response_model=list[SavedQueryResponse],
)
def get_saved_queries(
    db: Session = Depends(get_db),
) -> list[SavedQueryResponse]:
    service = QueryService(db)

    saved_queries = service.get_saved_queries()

    return [
        SavedQueryResponse.model_validate(
            item,
            from_attributes=True,
        )
        for item in saved_queries
    ]


@router.get(
    "/saved/{query_id}",
    response_model=SavedQueryResponse,
)
def get_saved_query(
    query_id: int,
    db: Session = Depends(get_db),
) -> SavedQueryResponse:
    service = QueryService(db)

    saved_query = service.get_saved_query(query_id)

    if saved_query is None:
        raise HTTPException(
            status_code=404,
            detail=f"Saved query not found: {query_id}",
        )

    return SavedQueryResponse.model_validate(
        saved_query,
        from_attributes=True,
    )


@router.patch(
    "/saved/{query_id}",
    response_model=SavedQueryResponse,
)
def update_saved_query(
    query_id: int,
    request: SavedQueryUpdateRequest,
    db: Session = Depends(get_db),
) -> SavedQueryResponse:
    service = QueryService(db)

    update_data = request.model_dump(
        exclude_unset=True,
    )

    saved_query = service.update_saved_query(
        query_id,
        **update_data,
    )

    if saved_query is None:
        raise HTTPException(
            status_code=404,
            detail=f"Saved query not found: {query_id}",
        )

    return SavedQueryResponse.model_validate(
        saved_query,
        from_attributes=True,
    )


@router.delete(
    "/saved/{query_id}",
    status_code=204,
)
def delete_saved_query(
    query_id: int,
    db: Session = Depends(get_db),
) -> None:
    service = QueryService(db)

    deleted = service.delete_saved_query(query_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Saved query not found: {query_id}",
        )
