from fastapi import FastAPI

app = FastAPI(
    title="BigData Smart Transportation Platform",
    description="Big Data Analytics Platform for Smart Transportation",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "BigData Smart Transportation Platform",
        "status": "ok",
        "version": "0.1.0",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }