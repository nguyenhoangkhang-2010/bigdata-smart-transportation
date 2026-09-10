from typing import Any

from pydantic import BaseModel


class GraphQueryRequest(BaseModel):
    query: str
    source_column: str
    target_column: str
    relationship_column: str | None = None
    node_label_column: str | None = None


class GraphNode(BaseModel):
    id: str
    label: str
    data: dict[str, Any] = {}


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship: str | None = None
    data: dict[str, Any] = {}


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]