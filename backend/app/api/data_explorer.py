from fastapi import APIRouter, HTTPException, Query

from backend.app.schemas.data_explorer import (
    ColumnInfo,
    DatabaseInfo,
    DataPreview,
    PartitionInfo,
    TableInfo,
)
from backend.app.services.data_explorer import DataExplorerService


router = APIRouter(
    prefix="/api/data-explorer",
    tags=["data-explorer"],
)


@router.get(
    "/databases",
    response_model=list[DatabaseInfo],
)
def get_databases() -> list[DatabaseInfo]:
    service = DataExplorerService()

    return service.get_databases()


@router.get(
    "/tables",
    response_model=list[TableInfo],
)
def get_tables(
    database: str | None = None,
) -> list[TableInfo]:
    service = DataExplorerService()

    try:
        return service.get_tables(database)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "/tables/{table}/schema",
    response_model=list[ColumnInfo],
)
def get_schema(
    table: str,
) -> list[ColumnInfo]:
    service = DataExplorerService()

    try:
        return service.get_schema(table)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "/tables/{table}/partitions",
    response_model=list[PartitionInfo],
)
def get_partitions(
    table: str,
) -> list[PartitionInfo]:
    service = DataExplorerService()

    try:
        return service.get_partitions(table)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "/tables/{table}/preview",
    response_model=DataPreview,
)
def get_preview(
    table: str,
    limit: int = Query(default=100),
) -> DataPreview:
    service = DataExplorerService()

    try:
        return service.get_preview(table, limit)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc