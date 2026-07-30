import os
import subprocess
import sys
import logging
from typing import List, Dict, Optional, Any
from fuzzywuzzy import process
from livekit.agents import function_tool
import asyncio

try:
    import pygetwindow as gw
except ImportError:
    gw = None

sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def focus_window(title_keyword: str) -> bool:
    """Attempts to bring a window containing title_keyword into focus.

    Args:
        title_keyword (str): Partial or full window title keyword.

    Returns:
        bool: True if window was found and focused, False otherwise.
    """
    if not gw:
        logger.warning("⚠️ pygetwindow library is not available.")
        return False

    await asyncio.sleep(1.5)
    title_keyword = title_keyword.lower().strip()

    try:
        for window in gw.getAllWindows():
            if title_keyword in window.title.lower():
                if window.isMinimized:
                    window.restore()
                window.activate()
                logger.info(f"🪟 Window focused: {window.title}")
                return True
    except Exception as e:
        logger.error(f"❌ Error focusing window: {e}")

    logger.warning("⚠️ No matching window found to focus.")
    return False


EXCLUDED_DIRS = {
    "$RECYCLE.BIN",
    "System Volume Information",
    ".git",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".venv",
}


async def index_files(base_dirs: List[str], max_depth: int = 5) -> List[Dict[str, str]]:
    """Indexes files recursively from specified base directories up to a max depth.

    Args:
        base_dirs (List[str]): List of directory paths to index.
        max_depth (int): Maximum directory recursion depth (default 5).

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing file metadata.
    """
    file_index = []
    for base_dir in base_dirs:
        base_path = os.path.abspath(base_dir)
        if not os.path.exists(base_path):
            logger.warning(f"⚠️ Directory does not exist, skipping: {base_dir}")
            continue
        try:
            base_depth = base_path.rstrip(os.sep).count(os.sep)
            for root, dirs, files in os.walk(base_path, topdown=True):
                # Prune excluded system/cache and hidden directories in-place
                dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith('.')]
                
                current_depth = root.rstrip(os.sep).count(os.sep) - base_depth
                if current_depth >= max_depth:
                    dirs.clear()
                    continue

                for f in files:
                    if f.startswith('.'):
                        continue
                    file_index.append({
                        "name": f,
                        "path": os.path.join(root, f),
                        "type": "file"
                    })
        except Exception as e:
            logger.error(f"❌ Failed to index directory {base_dir}: {e}")

    logger.info(f"✅ Indexed total {len(file_index)} files from valid directories.")
    return file_index


async def search_file(query: str, index: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """Fuzzy searches for a file name within the indexed file list.

    Args:
        query (str): Target filename query.
        index (List[Dict[str, str]]): List of indexed file dictionaries.

    Returns:
        Optional[Dict[str, str]]: Matched file dictionary or None.
    """
    choices = [item["name"] for item in index]
    if not choices:
        logger.warning("⚠️ No files in index to match against.")
        return None

    best_match_result = process.extractOne(query, choices)
    if not best_match_result:
        return None

    best_match, score = best_match_result[0], best_match_result[1]
    logger.info(f"🔍 Matched '{query}' to '{best_match}' (Score: {score})")
    if score > 70:
        for item in index:
            if item["name"] == best_match:
                return item
    return None


async def open_file(item: Dict[str, str]) -> str:
    """Launches the specified file with system default handler and focuses its window.

    Args:
        item (Dict[str, str]): File item containing 'path' and 'name'.

    Returns:
        str: Status message of the action.
    """
    try:
        path = item["path"]
        logger.info(f"📂 Opening file: {path}")
        if os.name == 'nt':
            os.startfile(path)
        else:
            subprocess.call(['open' if sys.platform == 'darwin' else 'xdg-open', path])
        await focus_window(item["name"])
        return f"✅ File successfully opened: {item['name']}"
    except Exception as e:
        logger.error(f"❌ Failed to open file: {e}")
        return f"❌ Failed to open file: {e}"


async def handle_command(command: str, index: List[Dict[str, str]]) -> str:
    """Processes search and open operations for a user command.

    Args:
        command (str): File search query.
        index (List[Dict[str, str]]): File metadata index.

    Returns:
        str: Execution result status string.
    """
    item = await search_file(command, index)
    if item:
        return await open_file(item)
    else:
        logger.warning("❌ File not found.")
        return "❌ File not found."


@function_tool
async def Play_file(name: str) -> str:
    """LiveKit agent tool to search for and open a requested file across target directories.

    Args:
        name (str): Name or description of the file to play/open.

    Returns:
        str: Status message for agent feedback.
    """
    folders_to_index = [
        "D:/",
        "C:/Users/bhish/Desktop",
        "C:/Users/bhish/Documents",
        "C:/Users/bhish/Downloads/Telegram Desktop"
    ]
    index = await index_files(folders_to_index)
    command = name.strip()
    return await handle_command(command, index)