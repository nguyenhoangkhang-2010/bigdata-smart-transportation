from fastapi import FastAPI

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
    return {
        "status": "healthy",
        "environment": settings.environment,
    }