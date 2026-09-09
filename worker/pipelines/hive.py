from collections.abc import Iterable

from pyhive import hive

from backend.app.core.config import get_settings


class HivePipelineRunner:
    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        database: str | None = None,
    ) -> None:
        settings = get_settings()

        self.host = host or settings.hive_host
        self.port = port or settings.hive_port
        self.database = database or settings.hive_database

    def execute(
        self,
        statements: Iterable[str],
    ) -> None:
        connection = hive.connect(
            host=self.host,
            port=self.port,
            database=self.database,
        )

        try:
            cursor = connection.cursor()

            try:
                for statement in statements:
                    cursor.execute(statement)
            finally:
                cursor.close()
        finally:
            connection.close()