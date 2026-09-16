import re
from typing import Any

from pyhive import hive

from backend.app.core.config import get_settings


_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class DataExplorerService:
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

    def _validate_identifier(self, value: str) -> str:
        if not _IDENTIFIER_PATTERN.fullmatch(value):
            raise ValueError(f"Invalid Hive identifier: {value}")

        return value

    def _execute_query(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        connection = hive.connect(
            host=self.host,
            port=self.port,
            database=self.database,
        )

        try:
            cursor = connection.cursor()

            try:
                cursor.execute(query)

                columns = [
                    description[0]
                    for description in cursor.description or []
                ]

                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            finally:
                cursor.close()

        finally:
            connection.close()

    def get_databases(self) -> list[dict[str, Any]]:
        rows = self._execute_query("SHOW DATABASES")

        return [
            {
                "name": next(iter(row.values())),
            }
            for row in rows
        ]

    def get_tables(
        self,
        database: str | None = None,
    ) -> list[dict[str, Any]]:
        target_database = self._validate_identifier(
            database or self.database
        )

        rows = self._execute_query(
            f"SHOW TABLES IN {target_database}"
        )

        return [
            {
                "name": next(iter(row.values())),
            }
            for row in rows
        ]

    def get_schema(
        self,
        table: str,
    ) -> list[dict[str, Any]]:
        target_table = self._validate_identifier(table)

        rows = self._execute_query(
            f"DESCRIBE {target_table}"
        )

        result = []

        for row in rows:
            values = list(row.values())

            if not values or not values[0]:
                continue

            result.append(
                {
                    "name": values[0],
                    "data_type": values[1] if len(values) > 1 else "",
                    "comment": values[2] if len(values) > 2 else None,
                }
            )

        return result

    def get_partitions(
        self,
        table: str,
    ) -> list[dict[str, Any]]:
        target_table = self._validate_identifier(table)

        rows = self._execute_query(
            f"SHOW PARTITIONS {target_table}"
        )

        return [
            {
                "name": next(iter(row.values())),
            }
            for row in rows
        ]

    def get_preview(
        self,
        table: str,
        limit: int = 100,
    ) -> dict[str, Any]:
        target_table = self._validate_identifier(table)

        if limit < 1 or limit > 1000:
            raise ValueError("limit must be between 1 and 1000")

        rows = self._execute_query(
            f"SELECT * FROM {target_table} LIMIT {limit}"
        )

        columns = list(rows[0].keys()) if rows else []

        return {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
        }

    def get_statistics(
        self,
        table: str,
    ) -> dict[str, Any]:
        target_table = self._validate_identifier(table)

        rows = self._execute_query(
            f"DESCRIBE FORMATTED {target_table}"
        )

        metadata = self._extract_formatted_metadata(rows)

        return {
            "row_count": self._parse_int(
                metadata.get("numRows")
            ),
            "file_count": self._parse_int(
                metadata.get("numFiles")
            ),
            "total_size_bytes": self._parse_int(
                metadata.get("totalSize")
            ),
        }

    def get_storage(
        self,
        table: str,
    ) -> dict[str, Any]:
        target_table = self._validate_identifier(table)

        rows = self._execute_query(
            f"DESCRIBE FORMATTED {target_table}"
        )

        metadata = self._extract_formatted_metadata(rows)

        return {
            "location": metadata.get("location"),
            "input_format": metadata.get("inputFormat"),
            "output_format": metadata.get("outputFormat"),
            "table_type": metadata.get("tableType"),
        }

    @staticmethod
    def _extract_formatted_metadata(
        rows: list[dict[str, Any]],
    ) -> dict[str, str]:
        metadata: dict[str, str] = {}

        for row in rows:
            values = list(row.values())

            if len(values) < 2:
                continue

            key = str(values[0]).strip()
            value = values[1]

            if not key or value is None:
                continue

            metadata[key] = str(value).strip()

        return metadata

    @staticmethod
    def _parse_int(value: str | None) -> int | None:
        if value is None:
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None