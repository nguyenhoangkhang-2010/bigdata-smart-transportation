import time
from typing import Any

from pyhive import hive

from backend.app.core.config import get_settings


class QueryService:
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

    def _execute_query(
        self,
        query: str,
    ) -> tuple[list[str], list[dict[str, Any]], float]:
        connection = hive.connect(
            host=self.host,
            port=self.port,
            database=self.database,
        )

        start_time = time.perf_counter()

        try:
            cursor = connection.cursor()

            try:
                cursor.execute(query)

                columns = [
                    description[0]
                    for description in cursor.description or []
                ]

                rows = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

                execution_time_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                return columns, rows, execution_time_ms

            finally:
                cursor.close()

        finally:
            connection.close()

    def execute_query(
        self,
        query: str,
    ) -> dict[str, Any]:
        columns, rows, execution_time_ms = self._execute_query(query)

        return {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "execution_time_ms": round(execution_time_ms, 2),
        }

    def explain_query(
        self,
        query: str,
    ) -> dict[str, Any]:
        columns, rows, execution_time_ms = self._execute_query(
            f"EXPLAIN {query}"
        )

        return {
            "plan": rows,
            "execution_time_ms": round(execution_time_ms, 2),
        }