from pydantic import BaseModel, Field


class CurrentWeather(BaseModel):
    time: str
    interval: int
    temperature: float
    windspeed: float
    winddirection: int
    is_day: int
    weathercode: int


class HourlyWeather(BaseModel):
    time: str
    temperature_2m: float
    apparent_temperature: float
    precipitation_probability: float
    precipitation: float
    weather_code: int
    wind_speed_10m: float


class LocationMatch(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: str
    admin1: str | None = None


class Coords(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)

