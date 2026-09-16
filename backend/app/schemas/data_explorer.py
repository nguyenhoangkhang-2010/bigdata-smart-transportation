from typing import Any

from pydantic import BaseModel


class DatabaseInfo(BaseModel):
    name: str


class TableInfo(BaseModel):
    name: str


class ColumnInfo(BaseModel):
    name: str
    data_type: str
    comment: str | None = None


class PartitionInfo(BaseModel):
    name: str


class DataPreview(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int


class TableStatistics(BaseModel):
    row_count: int | None = None
    file_count: int | None = None
    total_size_bytes: int | None = None


class TableStorage(BaseModel):
    location: str | None = None
    input_format: str | None = None
    output_format: str | None = None
    table_type: str | None = None