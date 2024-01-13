import os
import logging
import requests

from dotenv import load_dotenv

load_dotenv()

LAT, LONG = 41.311081, 69.240562
CHAT_ID = os.getenv("CHAT_ID")


async def show_daily_weather(bot):
    try:
        params = {
            "lat": LAT,
            "lon": LONG,
            "appid": os.getenv("WEATHER_API_KEY"),
            "units": "metric",
        }
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params).json()
        weather = response["weather"][0]["main"]
        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        await bot.send_message(CHAT_ID, f"Today's weather: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%")
    except Exception as e:
        logging.error(e)
        await bot.send_message(CHAT_ID, "Something went wrong")