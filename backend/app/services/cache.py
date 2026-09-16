import hashlib
import json
from typing import Any

from backend.app.core.config import get_settings
from backend.app.core.redis import get_redis_client


class QueryCache:
    def __init__(self) -> None:
        settings = get_settings()

        self.redis = get_redis_client()
        self.ttl_seconds = settings.redis_cache_ttl_seconds

    def _build_key(self, query: str) -> str:
        query_hash = hashlib.sha256(
            query.strip().encode("utf-8")
        ).hexdigest()

        return f"query:{query_hash}"

    def get(self, query: str) -> dict[str, Any] | None:
        key = self._build_key(query)
        cached_value = self.redis.get(key)

        if cached_value is None:
            return None

        return json.loads(cached_value)

    def set(
        self,
        query: str,
        result: dict[str, Any],
    ) -> None:
        key = self._build_key(query)

        self.redis.setex(
            key,
            self.ttl_seconds,
            json.dumps(result, default=str),
        )