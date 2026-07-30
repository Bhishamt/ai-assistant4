"""
Unit Test Suite for JARVIS AI Assistant Core Tools and Safe Controller.
"""

import unittest
import asyncio
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from keyboard_mouse_CTRL import SafeController
from jarvis_file_opener import search_file
from jarvis_window_CTRL import search_item, APP_MAPPINGS


class TestSafeController(unittest.TestCase):
    """Test suite for SafeController authentication and safety controls."""

    def setUp(self):
        self.controller = SafeController()

    def test_activation_success(self):
        self.controller.activate("my_secret_token")
        self.assertTrue(self.controller.is_active())

    def test_activation_failure(self):
        self.controller.activate("invalid_token")
        self.assertFalse(self.controller.is_active())

    def test_deactivation(self):
        self.controller.activate("my_secret_token")
        self.controller.deactivate()
        self.assertFalse(self.controller.is_active())

    def test_resolve_key_special(self):
        key = self.controller.resolve_key("enter")
        self.assertIsNotNone(key)

    def test_resolve_key_character(self):
        key = self.controller.resolve_key("a")
        self.assertEqual(key, "a")

    def test_inactive_controller_blocks_action(self):
        result = asyncio.run(self.controller.move_cursor("left", 50))
        self.assertIn("Controller is inactive", result)


class TestFuzzySearchAndMappings(unittest.TestCase):
    """Test suite for fuzzy file searching and application mappings."""

    def test_search_file_match(self):
        index = [
            {"name": "test_document.txt", "path": "C:/docs/test_document.txt", "type": "file"},
            {"name": "image.png", "path": "C:/docs/image.png", "type": "file"},
        ]
        match = asyncio.run(search_file("test_document", index))
        self.assertIsNotNone(match)
        self.assertEqual(match["name"], "test_document.txt")

    def test_search_file_no_match(self):
        index = [
            {"name": "notes.txt", "path": "C:/docs/notes.txt", "type": "file"}
        ]
        match = asyncio.run(search_file("completely_unrelated_xyz", index))
        self.assertIsNone(match)

    def test_search_item_folder(self):
        index = [
            {"name": "Projects", "path": "D:/Projects", "type": "folder"},
            {"name": "Downloads", "path": "D:/Downloads", "type": "folder"}
        ]
        match = asyncio.run(search_item("Projects", index, "folder"))
        self.assertIsNotNone(match)
        self.assertEqual(match["name"], "Projects")

    def test_app_mappings_entries(self):
        self.assertIn("notepad", APP_MAPPINGS)
        self.assertIn("chrome", APP_MAPPINGS)
        self.assertIn("terminal", APP_MAPPINGS)
        self.assertEqual(APP_MAPPINGS["terminal"], "wt")

    def test_index_files_excluded_dirs_and_depth(self):
        from jarvis_file_opener import index_files
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as tmpdir:
            normal_dir = os.path.join(tmpdir, "documents")
            excluded_dir = os.path.join(tmpdir, ".git")
            os.makedirs(normal_dir)
            os.makedirs(excluded_dir)

            with open(os.path.join(normal_dir, "doc.txt"), "w") as f:
                f.write("test")
            with open(os.path.join(excluded_dir, "config"), "w") as f:
                f.write("git config")

            indexed = asyncio.run(index_files([tmpdir], max_depth=3))
            filenames = [item["name"] for item in indexed]
            self.assertIn("doc.txt", filenames)
            self.assertNotIn("config", filenames)


class TestWeatherAndSearchTools(unittest.TestCase):
    """Test suite for weather and web search function tools."""

    def test_get_current_datetime(self):
        from jarvis_google_search import get_current_datetime
        result = asyncio.run(get_current_datetime())
        self.assertIsInstance(result, str)
        self.assertIn("T", result)

    def test_get_city_from_file(self):
        from jarvis_get_weather import get_city_from_file
        city = get_city_from_file()
        self.assertIsInstance(city, str)

    def test_google_search_missing_keys(self):
        from jarvis_google_search import google_search
        import os
        orig_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
        if "GOOGLE_SEARCH_API_KEY" in os.environ:
            del os.environ["GOOGLE_SEARCH_API_KEY"]
        try:
            result = asyncio.run(google_search("python"))
            self.assertIn("missing", result.lower())
        finally:
            if orig_key:
                os.environ["GOOGLE_SEARCH_API_KEY"] = orig_key

    def test_get_weather_missing_key(self):
        from jarvis_get_weather import get_weather
        import os
        orig_key = os.environ.get("OPENWEATHER_API_KEY")
        if "OPENWEATHER_API_KEY" in os.environ:
            del os.environ["OPENWEATHER_API_KEY"]
        try:
            result = asyncio.run(get_weather("London"))
            self.assertTrue("openweather" in result.lower() or "missing" in result.lower())
        finally:
            if orig_key:
                os.environ["OPENWEATHER_API_KEY"] = orig_key

    def test_get_weather_timeout(self):
        from jarvis_get_weather import get_weather
        import os
        from unittest.mock import patch
        import requests
        with patch("requests.get", side_effect=requests.exceptions.Timeout("Connection timed out")):
            orig_key = os.environ.get("OPENWEATHER_API_KEY")
            os.environ["OPENWEATHER_API_KEY"] = "fake_key"
            try:
                result = asyncio.run(get_weather("London"))
                self.assertIn("timed out", result.lower())
            finally:
                if orig_key:
                    os.environ["OPENWEATHER_API_KEY"] = orig_key
                else:
                    os.environ.pop("OPENWEATHER_API_KEY", None)

    def test_google_search_timeout(self):
        from jarvis_google_search import google_search
        import os
        from unittest.mock import patch
        import requests
        with patch("requests.get", side_effect=requests.exceptions.Timeout("Connection timed out")):
            orig_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
            orig_cx = os.environ.get("SEARCH_ENGINE_ID")
            os.environ["GOOGLE_SEARCH_API_KEY"] = "fake_key"
            os.environ["SEARCH_ENGINE_ID"] = "fake_cx"
            try:
                result = asyncio.run(google_search("python"))
                self.assertIn("timed out", result.lower())
            finally:
                if orig_key:
                    os.environ["GOOGLE_SEARCH_API_KEY"] = orig_key
                else:
                    os.environ.pop("GOOGLE_SEARCH_API_KEY", None)
                if orig_cx:
                    os.environ["SEARCH_ENGINE_ID"] = orig_cx
                else:
                    os.environ.pop("SEARCH_ENGINE_ID", None)



class TestAgentEnvironment(unittest.TestCase):
    """Test suite for agent environment configuration validation."""

    def test_validate_environment_with_vars(self):
        from agent import validate_environment
        import os
        orig_vars = {v: os.environ.get(v) for v in ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]}
        try:
            os.environ["LIVEKIT_URL"] = "wss://test.livekit.cloud"
            os.environ["LIVEKIT_API_KEY"] = "test_key"
            os.environ["LIVEKIT_API_SECRET"] = "test_secret"
            self.assertTrue(validate_environment())
        finally:
            for k, v in orig_vars.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

    def test_validate_environment_missing_vars(self):
        from agent import validate_environment
        import os
        orig_vars = {v: os.environ.get(v) for v in ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]}
        try:
            os.environ.pop("LIVEKIT_URL", None)
            self.assertFalse(validate_environment())
        finally:
            for k, v in orig_vars.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v


if __name__ == "__main__":
    unittest.main()

