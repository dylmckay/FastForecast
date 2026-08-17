from fastapi import FastAPI

app = FastAPI(
    title="FastForecast",
    description="A weather API built with FastAPI and using data from the Open-Meteo API.",
    version="0.0.1",
)
