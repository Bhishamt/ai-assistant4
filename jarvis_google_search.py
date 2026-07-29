# jarvis_google_search.py
import os
import asyncio
import requests
import logging
from dotenv import load_dotenv
from livekit.agents import function_tool
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@function_tool
async def google_search(query: str) -> str:
    """
    Perform a Google Custom Search for the given query and return top results.
    
    Args:
        query: The search query string.
    """
    logger.info(f"Query प्राप्त हुई: {query}")

    api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")

    if not api_key or not search_engine_id:
        logger.error("API key या Search Engine ID missing है।")
        return "Environment variables में API key या Search Engine ID missing है।"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "num": 3
    }

    try:
        logger.info("Google Custom Search API को request भेजी जा रही है...")
        response = await asyncio.to_thread(requests.get, url, params=params, timeout=10)

        if response.status_code != 200:
            logger.error(f"Google API में error आया: {response.status_code} - {response.text}")
            return f"Google Search API में error आया: {response.status_code} - {response.text}"

        data = response.json()
        results = data.get("items", [])

        if not results:
            logger.info("कोई results नहीं मिले।")
            return "कोई results नहीं मिले।"

        formatted = ""
        logger.info("Search results:")
        for i, item in enumerate(results, start=1):
            title = item.get("title", "No title")
            link = item.get("link", "No link")
            snippet = item.get("snippet", "")
            formatted += f"{i}. {title}\n{link}\n{snippet}\n\n"
            logger.info(f"{i}. {title}\n{link}\n{snippet}\n")

        return formatted.strip()
    except Exception as e:
        logger.exception(f"Google search request failed: {e}")
        return f"Search execution failed: {e}"

@function_tool
async def get_current_datetime() -> str:
    """Return the current system date and time in ISO format."""
    return datetime.now().isoformat()
