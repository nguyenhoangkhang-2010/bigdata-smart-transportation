from datetime import date
from typing import Any

from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_trips: int
    vendor_count: int
    total_revenue: float | None
    avg_trip_distance: float | None
    avg_trip_duration_minutes: float | None
    avg_passenger_count: float | None


class DailyAnalytics(BaseModel):
    pickup_date: date
    trip_count: int
    total_revenue: float | None
    avg_trip_amount: float | None
    avg_trip_distance: float | None
    avg_trip_duration_minutes: float | None
    avg_passenger_count: float | None


class HourlyAnalytics(BaseModel):
    pickup_hour: int
    trip_count: int
    total_revenue: float | None
    avg_trip_amount: float | None
    avg_trip_distance: float | None
    avg_trip_duration_minutes: float | None


class WeekdayAnalytics(BaseModel):
    pickup_day_of_week: int
    trip_count: int
    total_revenue: float | None
    avg_trip_amount: float | None
    avg_trip_distance: float | None
    avg_trip_duration_minutes: float | None


class PaymentAnalytics(BaseModel):
    payment_type: int
    trip_count: int
    total_revenue: float | None
    avg_trip_amount: float | None
    avg_tip_amount: float | None


class LocationAnalytics(BaseModel):
    location_id: int
    trip_count: int
    total_revenue: float | None
    avg_trip_amount: float | None
    avg_trip_distance: float | None
    avg_trip_duration_minutes: float | None


class AnalyticsResponse(BaseModel):
    data: list[dict[str, Any]]