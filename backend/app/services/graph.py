from typing import Any

from pyhive import hive

from backend.app.core.config import get_settings


class GraphService:
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

    def query_graph(
        self,
        query: str,
        source_column: str,
        target_column: str,
        relationship_column: str | None = None,
        node_label_column: str | None = None,
    ) -> dict[str, Any]:
        rows = self._execute_query(query)

        nodes: dict[str, dict[str, Any]] = {}
        edges: list[dict[str, Any]] = []

        for index, row in enumerate(rows):
            source_value = row.get(source_column)
            target_value = row.get(target_column)

            if source_value is None or target_value is None:
                continue

            source_id = str(source_value)
            target_id = str(target_value)

            source_label = (
                str(row.get(node_label_column))
                if node_label_column and row.get(node_label_column) is not None
                else source_id
            )

            target_label = (
                str(row.get(node_label_column))
                if node_label_column and row.get(node_label_column) is not None
                else target_id
            )

            nodes.setdefault(
                source_id,
                {
                    "id": source_id,
                    "label": source_label,
                    "data": {},
                },
            )

            nodes.setdefault(
                target_id,
                {
                    "id": target_id,
                    "label": target_label,
                    "data": {},
                },
            )

            relationship = (
                str(row.get(relationship_column))
                if relationship_column
                and row.get(relationship_column) is not None
                else None
            )

            edges.append(
                {
                    "id": f"{source_id}-{target_id}-{index}",
                    "source": source_id,
                    "target": target_id,
                    "relationship": relationship,
                    "data": {},
                }
            )

        return {
            "nodes": list(nodes.values()),
            "edges": edges,
        }