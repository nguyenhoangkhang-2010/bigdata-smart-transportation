import json
import re
import time
from typing import Any

from pyhive import hive

from backend.app.core.config import get_settings
from backend.app.services.cache import QueryCache
from backend.app.schemas.analytics import AnalyticsRequest


_IDENTIFIER_PATTERN = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?$"
)


class AnalyticsService:
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
        self.cache = QueryCache()

    @staticmethod
    def _validate_identifier(value: str) -> str:
        if not _IDENTIFIER_PATTERN.fullmatch(value):
            raise ValueError(
                f"Invalid SQL identifier: {value}"
            )

        return value

    @classmethod
    def _validate_identifiers(
        cls,
        values: list[str],
    ) -> list[str]:
        return [
            cls._validate_identifier(value)
            for value in values
        ]

    @staticmethod
    def _build_measure_expression(
        column: str,
        aggregation: str,
    ) -> str:
        if aggregation == "count":
            if column == "*":
                return "COUNT(*)"
            return f"COUNT({column})"

        if aggregation == "count_distinct":
            return f"COUNT(DISTINCT {column})"

        return f"{aggregation.upper()}({column})"

    @classmethod
    def _build_query(
        cls,
        request: AnalyticsRequest,
    ) -> str:
        table = cls._validate_identifier(request.table)

        dimensions = cls._validate_identifiers(
            request.dimensions
        )

        measure_expressions: list[str] = []

        for measure in request.measures:
            column = (
                "*"
                if measure.column == "*"
                else cls._validate_identifier(
                    measure.column
                )
            )

            measure_expressions.append(
                cls._build_measure_expression(
                    column,
                    measure.aggregation,
                )
                + f" AS {measure.aggregation}_{column.replace('.', '_').replace('*', 'all')}"
            )

        if not dimensions and not measure_expressions:
            raise ValueError(
                "At least one dimension or measure is required"
            )

        select_parts = [
            *dimensions,
            *measure_expressions,
        ]

        query = (
            "SELECT "
            + ", ".join(select_parts)
            + f" FROM {table}"
        )

        if request.filters:
            filter_parts: list[str] = []

            for item in request.filters:
                column = cls._validate_identifier(
                    item.column
                )

                if item.operator not in {
                    "=",
                    "!=",
                    ">",
                    ">=",
                    "<",
                    "<=",
                }:
                    raise ValueError(
                        f"Unsupported filter operator: "
                        f"{item.operator}"
                    )

                value = item.value

                if isinstance(value, str):
                    escaped = value.replace(
                        "'",
                        "''",
                    )
                    sql_value = f"'{escaped}'"
                elif value is None:
                    raise ValueError(
                        "NULL filters are not supported"
                    )
                elif isinstance(value, bool):
                    sql_value = (
                        "TRUE"
                        if value
                        else "FALSE"
                    )
                elif isinstance(value, (int, float)):
                    sql_value = str(value)
                else:
                    raise ValueError(
                        "Unsupported filter value type"
                    )

                filter_parts.append(
                    f"{column} {item.operator} "
                    f"{sql_value}"
                )

            query += " WHERE " + " AND ".join(
                filter_parts
            )

        if dimensions:
            query += (
                " GROUP BY "
                + ", ".join(dimensions)
            )

        if request.order_by:
            order_parts: list[str] = []

            for item in request.order_by:
                column = cls._validate_identifier(
                    item.column
                )

                direction = item.direction.upper()

                order_parts.append(
                    f"{column} {direction}"
                )

            query += (
                " ORDER BY "
                + ", ".join(order_parts)
            )

        query += f" LIMIT {request.limit}"

        return query

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

                return (
                    columns,
                    rows,
                    execution_time_ms,
                )
            finally:
                cursor.close()
        finally:
            connection.close()

    def execute(
        self,
        request: AnalyticsRequest,
    ) -> dict[str, Any]:
        query = self._build_query(request)

        cache_key = json.dumps(
            {
                "query": query,
            },
            sort_keys=True,
        )

        cached_result = self.cache.get(
            cache_key
        )

        if cached_result is not None:
            return {
                **cached_result,
                "cache_status": "HIT",
            }

        (
            columns,
            rows,
            execution_time_ms,
        ) = self._execute_query(query)

        result = {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "execution_time_ms": round(
                execution_time_ms,
                2,
            ),
            "engine": "hive",
        }

        self.cache.set(
            cache_key,
            result,
        )

        return {
            **result,
            "cache_status": "MISS",
        }