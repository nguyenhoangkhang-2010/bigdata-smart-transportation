import time
from typing import Any

from pyhive import hive
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.config import get_settings
from backend.app.models.query_history import QueryHistory
from backend.app.models.saved_query import SavedQuery
from backend.app.services.cache import QueryCache


class QueryService:
    def __init__(
        self,
        db: Session,
        host: str | None = None,
        port: int | None = None,
        database: str | None = None,
    ) -> None:
        settings = get_settings()

        self.db = db
        self.host = host or settings.hive_host
        self.port = port or settings.hive_port
        self.database = database or settings.hive_database
        self.cache = QueryCache()

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

    def _save_history(
        self,
        *,
        query: str,
        engine: str,
        cache_status: str,
        execution_time_ms: float,
        row_count: int,
    ) -> None:
        history = QueryHistory(
            query=query,
            engine=engine,
            cache_status=cache_status,
            execution_time_ms=execution_time_ms,
            row_count=row_count,
        )

        self.db.add(history)
        self.db.commit()

    def execute_query(
        self,
        query: str,
    ) -> dict[str, Any]:
        normalized_query = query.strip()

        cached_result = self.cache.get(normalized_query)

        if cached_result is not None:
            result = {
                **cached_result,
                "engine": "hive",
                "cache_status": "HIT",
                "rows_scanned": None,
            }

            self._save_history(
                query=normalized_query,
                engine="hive",
                cache_status="HIT",
                execution_time_ms=result["execution_time_ms"],
                row_count=result["row_count"],
            )

            return result

        columns, rows, execution_time_ms = self._execute_query(
            normalized_query
        )

        execution_time_ms = round(
            execution_time_ms,
            2,
        )

        result = {
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "execution_time_ms": execution_time_ms,
        }

        self.cache.set(
            normalized_query,
            result,
        )

        response = {
            **result,
            "engine": "hive",
            "cache_status": "MISS",
            "rows_scanned": None,
        }

        self._save_history(
            query=normalized_query,
            engine="hive",
            cache_status="MISS",
            execution_time_ms=execution_time_ms,
            row_count=len(rows),
        )

        return response

    def explain_query(
        self,
        query: str,
    ) -> dict[str, Any]:
        normalized_query = query.strip()

        _, rows, execution_time_ms = self._execute_query(
            f"EXPLAIN {normalized_query}"
        )

        return {
            "plan": rows,
            "execution_time_ms": round(
                execution_time_ms,
                2,
            ),
            "engine": "hive",
        }

    def get_history(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[QueryHistory]:
        statement = (
            select(QueryHistory)
            .order_by(QueryHistory.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def create_saved_query(
        self,
        *,
        name: str,
        query: str,
        description: str | None,
    ) -> SavedQuery:
        saved_query = SavedQuery(
            name=name,
            query=query.strip(),
            description=description,
        )

        self.db.add(saved_query)
        self.db.commit()
        self.db.refresh(saved_query)

        return saved_query

    def get_saved_queries(self) -> list[SavedQuery]:
        statement = (
            select(SavedQuery)
            .order_by(SavedQuery.updated_at.desc())
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_saved_query(
        self,
        query_id: int,
    ) -> SavedQuery | None:
        return self.db.get(
            SavedQuery,
            query_id,
        )

    def update_saved_query(
        self,
        query_id: int,
        **updates: Any,
    ) -> SavedQuery | None:
        saved_query = self.get_saved_query(query_id)

        if saved_query is None:
            return None

        if "name" in updates:
            saved_query.name = updates["name"]

        if "query" in updates:
            saved_query.query = updates["query"].strip()

        if "description" in updates:
            saved_query.description = updates["description"]

        self.db.commit()
        self.db.refresh(saved_query)

        return saved_query

    def delete_saved_query(
        self,
        query_id: int,
    ) -> bool:
        saved_query = self.get_saved_query(query_id)

        if saved_query is None:
            return False

        self.db.delete(saved_query)
        self.db.commit()

        return True
