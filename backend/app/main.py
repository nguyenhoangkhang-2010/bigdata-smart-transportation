from fastapi import FastAPI
from sqlalchemy import text

from backend.app.api.analytics import router as analytics_router
from backend.app.api.query import router as query_router
from backend.app.api.data_explorer import router as data_explorer_router
from backend.app.api.graph import router as graph_router
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


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "status": "ok",
        "version": settings.app_version,
    }


@app.get("/health")
async def health() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "environment": settings.environment,
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "environment": settings.environment,
        }