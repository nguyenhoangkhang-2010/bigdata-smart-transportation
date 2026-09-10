from typing import Any

from pyhive import hive
from pymongo.errors import PyMongoError
from redis import Redis
from sqlalchemy import text

from backend.app.core.config import get_settings
from backend.app.core.database import engine
from backend.app.core.kafka import get_kafka_producer
from backend.app.core.mongodb import get_mongo_database
from backend.app.core.redis import get_redis_client


class SystemHealthService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def _check_postgresql(self) -> str:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            return "healthy"
        except Exception:
            return "unhealthy"

    def _check_mongodb(self) -> str:
        try:
            get_mongo_database().client.admin.command("ping")

            return "healthy"
        except PyMongoError:
            return "unhealthy"
        except Exception:
            return "unhealthy"

    def _check_redis(self) -> str:
        client: Redis = get_redis_client()

        try:
            return "healthy" if client.ping() else "unhealthy"
        except Exception:
            return "unhealthy"

    def _check_kafka(self) -> str:
        producer = get_kafka_producer()

        try:
            producer.list_topics(timeout=5)
            return "healthy"
        except Exception:
            return "unhealthy"

    def _check_hive(self) -> str:
        connection = None

        try:
            connection = hive.connect(
                host=self.settings.hive_host,
                port=self.settings.hive_port,
                database=self.settings.hive_database,
            )

            return "healthy"
        except Exception:
            return "unhealthy"
        finally:
            if connection is not None:
                connection.close()

    def get_health(self) -> dict[str, Any]:
        services = {
            "postgresql": {
                "status": self._check_postgresql(),
            },
            "mongodb": {
                "status": self._check_mongodb(),
            },
            "redis": {
                "status": self._check_redis(),
            },
            "kafka": {
                "status": self._check_kafka(),
            },
            "hive": {
                "status": self._check_hive(),
            },
        }

        overall_status = (
            "healthy"
            if all(
                service["status"] == "healthy"
                for service in services.values()
            )
            else "unhealthy"
        )

        return {
            "status": overall_status,
            "services": services,
            "environment": self.settings.environment,
        }