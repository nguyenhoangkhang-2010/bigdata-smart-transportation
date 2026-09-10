from fastapi import FastAPI
from sqlalchemy import text

from backend.app.api.analytics import router as analytics_router
from backend.app.api.query import router as query_router
from backend.app.api.data_explorer import router as data_explorer_router
from backend.app.api.graph import router as graph_router
from backend.app.api.lineage import router as lineage_router
from backend.app.api.system import router as system_router
from backend.app.core.config import get_settings
from backend.app.core.database import engine


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Big Data Analytics Platform for Smart Transportation",
)

app.include_router(analytics_router)
app.include_router(query_router)
app.include_router(data_explorer_router)
app.include_router(graph_router)
app.include_router(lineage_router)
app.include_router(system_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "status": "ok",
        "version": settings.app_version,
    }