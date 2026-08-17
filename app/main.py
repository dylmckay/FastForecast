import logging
import sys

from fastapi import FastAPI

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI(
    title="FastForecast",
    description="A weather API built with FastAPI and using data from the Open-Meteo API.",
    version="0.0.1",
)
