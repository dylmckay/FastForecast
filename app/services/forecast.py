import json
import logging

import httpx
from fastapi import HTTPException, status

from ..schemas.forecast import Coords, CurrentWeather, HourlyWeather, LocationMatch

logger = logging.getLogger(__name__)


def get_coords(match: LocationMatch) -> Coords:
    lat: float = match.latitude
    lon: float = match.longitude
    return Coords(lat=lat, lon=lon)


async def get_current_weather(coords: Coords) -> CurrentWeather:
    params = {
        "latitude": coords.lat,
        "longitude": coords.lon,
        "current_weather": True,
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url="https://api.open-meteo.com/v1/forecast", params=params
            )
            r.raise_for_status()
            r_json = r.json()["current_weather"]
            return CurrentWeather(**r_json)
    except (
        KeyError,
        json.JSONDecodeError,
        httpx.RequestError,
        httpx.HTTPStatusError,
    ) as exc:
        logger.error(f"Open-Meteo request failed: {exc}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)


async def get_hourly_weather(coords: Coords) -> list[HourlyWeather]:
    params = {
        "latitude": coords.lat,
        "longitude": coords.lon,
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation_probability",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
        ],
        "forecast_days": 1,
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://api.open-meteo.com/v1/forecast", params=params
            )
            r.raise_for_status()
            r_json = r.json()["hourly"]
            results: list[HourlyWeather] = []
            for row in zip(*r_json.values()):
                row_dict = dict(zip(r_json.keys(), row))
                results.append(HourlyWeather(**row_dict))
            return results
    except (
        KeyError,
        json.JSONDecodeError,
        httpx.RequestError,
        httpx.HTTPStatusError,
    ) as exc:
        logger.error(f"Open-Meteo request failed: {exc}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)


async def get_location_info(location_name: str) -> list[LocationMatch]:
    params = {"name": location_name}
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url="https://geocoding-api.open-meteo.com/v1/search", params=params
            )
            r.raise_for_status()
            results = r.json()["results"]
    except KeyError:
        logger.warning("No location matches found for that request.")
        results = []
    except (json.JSONDecodeError, httpx.RequestError, httpx.HTTPStatusError) as exc:
        logger.error(f"Open-Meteo request failed: {exc}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
    location_matches = [LocationMatch(**location) for location in results]
    return location_matches
