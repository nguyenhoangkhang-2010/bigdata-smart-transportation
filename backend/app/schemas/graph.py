from typing import Any

from pydantic import BaseModel, Field


class GraphQueryRequest(BaseModel):
    table: str
    source_column: str
    target_column: str
    relationship_column: str | None = None
    node_label_column: str | None = None


class GraphNode(BaseModel):
    id: str
    label: str
    data: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]