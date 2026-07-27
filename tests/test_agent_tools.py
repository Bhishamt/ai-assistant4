"""
Unit Test Suite for JARVIS AI Assistant Core Tools and Safe Controller.
"""

import unittest
import asyncio
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


if __name__ == "__main__":
    unittest.main()
