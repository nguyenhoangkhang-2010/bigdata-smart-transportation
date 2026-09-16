from pydantic import BaseModel


class ServiceHealth(BaseModel):
    status: str


class SystemHealthResponse(BaseModel):
    status: str
    services: dict[str, ServiceHealth]
    environment: str