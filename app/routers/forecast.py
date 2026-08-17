from fastapi import APIRouter

from ..schemas.forecast import CurrentWeather, HourlyWeather, LocationMatch
from ..services.forecast import (
    get_coords,
    get_current_weather,
    get_hourly_weather,
    get_location_info,
)

router = APIRouter(tags=["forecast"])


@router.get("/info/")
async def location_info(location: str) -> list[LocationMatch]:
    info = await get_location_info(location)
    return info


@router.post("/current/")
async def current_weather(location: LocationMatch) -> CurrentWeather:
    coords = get_coords(location)
    current_forecast = await get_current_weather(coords)
    return current_forecast


@router.post("/hourly/")
async def hourly_weather(location: LocationMatch) -> list[HourlyWeather]:
    coords = get_coords(location)
    hourly_forecast = await get_hourly_weather(coords)
    return hourly_forecast
