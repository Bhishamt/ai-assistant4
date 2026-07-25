# jarvis_get_weather.py
import os
import json
import requests
import logging
from dotenv import load_dotenv
from livekit.agents import function_tool

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_city_by_ip() -> str:
    """Attempt to detect the current user's city via IP service with a fallback default."""
    try:
        logger.info("IP के ज़रिए शहर detect करने की कोशिश की जा रही है")
        city = "Mandi, Thunag"
        if city:
            logger.info(f"IP से शहर Detect किया गया: {city}")
            return city
        else:
            logger.warning("City detect करने में विफल, default 'Himachal Pradesh Mandi, Thunag' इस्तेमाल किया जा रहा है।")
            return "Mandi, Thunag"
    except Exception as e:
        logger.error(f"IP से city detect करने में error आया: {e}")
        return "Himachal Pradesh, Mandi, Thunag"

def get_city_from_file() -> str:
    """Read city information from address configuration files (address.json or legacy addrees.json)."""
    for filename in ['address.json', 'addrees.json']:
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    city = data.get('city', '')
                    if city:
                        return city
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            logger.error(f"Error decoding {filename}.")
        except Exception as e:
            logger.error(f"Error reading {filename}: {e}")
    return ""

@function_tool
async def get_weather(city: str = "", use_address_file: bool = False) -> str:
    """
    Fetch the current weather information for a specified city or detected location.
    
    Args:
        city: Optional city name. If omitted, location will be auto-detected.
        use_address_file: If True, reads preferred city location from address JSON config.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        logger.error("OpenWeather API key missing है।")
        return "Environment variables में OpenWeather API key नहीं मिली।"

    if use_address_file:
        city_from_file = get_city_from_file()
        if city_from_file:
            city = city_from_file

    if not city:
        city = detect_city_by_ip()
        if not city:
            city = "Mandi, Thunag"

    logger.info(f"City के लिए weather fetch किया जा रहा है: {city}")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            logger.error(f"OpenWeather API error: {response.status_code} - {response.text}")
            return f"Error: {city} के लिए weather fetch नहीं कर पाए। कृपया city name चेक करें।"

        data = response.json()
        weather = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]
        feels_like = data["main"].get("feels_like", temperature)
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        result = (f"Weather in {city}:\n"
                  f"- Condition: {weather}\n"
                  f"- Temperature: {temperature}°C (Feels like: {feels_like}°C)\n"
                  f"- Humidity: {humidity}%\n"
                  f"- Wind Speed: {wind_speed} m/s")

        logger.info(f"Weather result:\n{result}")
        return result

    except Exception as e:
        logger.exception(f"Weather fetch करते समय exception आया: {e}")
        return "Weather fetch करते समय एक error आया"