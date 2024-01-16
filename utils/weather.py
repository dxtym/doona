import os
import logging
import requests
from utils.config import LAT, LONG
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")


async def show_daily_weather(bot: Bot) -> None:
    try:
        params = {
            "lat": LAT,
            "lon": LONG,
            "appid": os.getenv("WEATHER_API_KEY"),
            "units": "metric",
        }

        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather", 
            params=params).json()
        weather = response["weather"][0]["main"]
        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        
        await bot.send_message(
            CHAT_ID, 
            f"⛅ Weather:\nSummary: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%"
            )
    except Exception as e:
        logging.error(e)
        await bot.send_message(CHAT_ID, "Something went wrong")