from fastapi import APIRouter

from backend.app.schemas.analytics import (
    AnalyticsSummary,
    DailyAnalytics,
    HourlyAnalytics,
    PaymentAnalytics,
    WeekdayAnalytics,
)
from backend.app.services.analytics import AnalyticsService


router = APIRouter(
    prefix="/api/analytics",
    tags=["analytics"],
)


@router.get(
    "/summary",
    response_model=list[AnalyticsSummary],
)
def get_summary() -> list[AnalyticsSummary]:
    service = AnalyticsService()

    return service.get_summary()


@router.get(
    "/daily",
    response_model=list[DailyAnalytics],
)
def get_daily_summary() -> list[DailyAnalytics]:
    service = AnalyticsService()

    return service.get_daily_summary()


@router.get(
    "/hourly",
    response_model=list[HourlyAnalytics],
)
def get_hourly_summary() -> list[HourlyAnalytics]:
    service = AnalyticsService()

    return service.get_hourly_summary()


@router.get(
    "/weekday",
    response_model=list[WeekdayAnalytics],
)
def get_weekday_summary() -> list[WeekdayAnalytics]:
    service = AnalyticsService()

    return service.get_weekday_summary()


@router.get(
    "/payment",
    response_model=list[PaymentAnalytics],
)
def get_payment_summary() -> list[PaymentAnalytics]:
    service = AnalyticsService()

    return service.get_payment_summary()