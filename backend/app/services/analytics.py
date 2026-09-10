from typing import Any

from pyhive import hive

from backend.app.core.config import get_settings


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
                    for description in cursor.description
                ]

                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            finally:
                cursor.close()
        finally:
            connection.close()

    def get_summary(self) -> list[dict[str, Any]]:
        return self._execute_query(
            """
            SELECT
                COUNT(*) AS total_trips,
                COUNT(DISTINCT vendor_id) AS vendor_count,
                SUM(total_amount) AS total_revenue,
                AVG(trip_distance) AS avg_trip_distance,
                AVG(trip_duration_minutes) AS avg_trip_duration_minutes,
                AVG(passenger_count) AS avg_passenger_count
            FROM tlc_trips
            """
        )

    def get_daily_summary(self) -> list[dict[str, Any]]:
        return self._execute_query(
            """
            SELECT *
            FROM vw_tlc_daily_summary
            ORDER BY pickup_date
            """
        )

    def get_hourly_summary(self) -> list[dict[str, Any]]:
        return self._execute_query(
            """
            SELECT *
            FROM vw_tlc_hourly_summary
            ORDER BY pickup_hour
            """
        )

    def get_weekday_summary(self) -> list[dict[str, Any]]:
        return self._execute_query(
            """
            SELECT *
            FROM vw_tlc_weekday_summary
            ORDER BY pickup_day_of_week
            """
        )

    def get_payment_summary(self) -> list[dict[str, Any]]:
        return self._execute_query(
            """
            SELECT *
            FROM vw_tlc_payment_summary
            ORDER BY payment_type
            """
        )

    def get_pickup_location_summary(
        self,
    ) -> list[dict[str, Any]]:
        return self._execute_query(
            """
            SELECT *
            FROM vw_tlc_pickup_location_summary
            ORDER BY trip_count DESC
            """
        )

    def get_dropoff_location_summary(
        self,
    ) -> list[dict[str, Any]]:
        return self._execute_query(
            """
            SELECT *
            FROM vw_tlc_dropoff_location_summary
            ORDER BY trip_count DESC
            """
        )