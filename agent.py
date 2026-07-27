"""
Jarvis AI Assistant Entry Point
Voice-enabled multimodal AI agent using LiveKit and Google Realtime LLM models.
"""

import logging
import os
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)
from jarvis_prompts import behavior_prompts, Reply_prompts
from jarvis_google_search import google_search, get_current_datetime
from jarvis_get_weather import get_weather
from jarvis_window_CTRL import open, close, folder_file
from jarvis_file_opener import Play_file
from keyboard_mouse_CTRL import (
    move_cursor_tool,
    mouse_click_tool,
    scroll_cursor_tool,
    type_text_tool,
    press_key_tool,
    swipe_gesture_tool,
    press_hotkey_tool,
    control_volume_tool,
)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jarvis_agent")


def validate_environment() -> None:
    """Validates required environment variables for LiveKit and Google AI plugins."""
    required_vars = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.warning(
            f"⚠️ Missing environment variables: {', '.join(missing)}. "
            "Ensure they are specified in .env for full LiveKit functionality."
        )
    else:
        logger.info("✅ LiveKit environment configuration validated.")


class Assistant(Agent):
    """JARVIS Voice & Automation Agent."""
    
    def __init__(self) -> None:
        super().__init__(
            instructions=behavior_prompts,
            tools=[
                google_search,
                get_current_datetime,
                get_weather,
                open,
                close,
                folder_file,
                Play_file,
                move_cursor_tool,
                mouse_click_tool,
                scroll_cursor_tool,
                type_text_tool,
                press_key_tool,
                press_hotkey_tool,
                control_volume_tool,
                swipe_gesture_tool,
            ],
        )


async def entrypoint(ctx: agents.JobContext):
    """Main execution entrypoint for LiveKit Agent session."""
    validate_environment()
    logger.info("🚀 Starting JARVIS Agent session...")

    try:
        session = AgentSession(
            llm=google.beta.realtime.RealtimeModel(
                voice="Charon"
            )
        )

        await session.start(
            room=ctx.room,
            agent=Assistant(),
            room_input_options=RoomInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
                video_enabled=True,
            ),
        )

        await ctx.connect()

        await session.generate_reply(
            instructions=Reply_prompts
        )
        logger.info("✅ JARVIS Session successfully initialized.")
    except Exception as e:
        logger.error(f"❌ Error during agent session initialization: {e}")
        raise


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

