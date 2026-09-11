import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from backend.app.core.metrics import (
    HTTP_REQUESTS_IN_PROGRESS,
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
)


async def metrics_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    if request.url.path.rstrip("/") == "/metrics":
        return await call_next(request)

    start_time = time.perf_counter()

    HTTP_REQUESTS_IN_PROGRESS.inc()

    try:
        response = await call_next(request)

        duration = time.perf_counter() - start_time

        HTTP_REQUESTS_TOTAL.labels(
            method=request.method,
            path=request.url.path,
            status=str(response.status_code),
        ).inc()

        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=request.method,
            path=request.url.path,
        ).observe(duration)

        return response

    finally:
        HTTP_REQUESTS_IN_PROGRESS.dec()