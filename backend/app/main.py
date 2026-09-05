from fastapi import FastAPI
from sqlalchemy import text

from backend.app.core.database import engine
from backend.app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Big Data Analytics Platform for Smart Transportation",
)


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