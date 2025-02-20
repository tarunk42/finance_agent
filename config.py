import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

SERP_API_KEY = os.getenv("SERP_API_KEY")

FMP_API_KEY = os.getenv("FMP_API_KEY")

