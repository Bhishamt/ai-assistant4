# keyboard_mouse_CTRL.py
import pyautogui
import asyncio
import time
from datetime import datetime
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from typing import List, Union, Any, Dict, Optional
from livekit.agents import function_tool

# ---------------------
# SafeController Class
# ---------------------
class SafeController:
    """Safe controller class to manage keyboard and mouse interactions with security checks."""

    def __init__(self) -> None:
        self.active: bool = False
        self.activation_time: Optional[float] = None
        self.keyboard: KeyboardController = KeyboardController()
        self.mouse: MouseController = MouseController()
        self.valid_keys = set("abcdefghijklmnopqrstuvwxyz1234567890")
        self.special_keys: Dict[str, Any] = {
            "enter": Key.enter, "space": Key.space, "tab": Key.tab,
            "shift": Key.shift, "ctrl": Key.ctrl, "alt": Key.alt,
            "esc": Key.esc, "backspace": Key.backspace, "delete": Key.delete,
            "up": Key.up, "down": Key.down, "left": Key.left, "right": Key.right,
            "caps_lock": Key.caps_lock, "cmd": Key.cmd, "win": Key.cmd,
            "home": Key.home, "end": Key.end,
            "page_up": Key.page_up, "page_down": Key.page_down
        }

    def resolve_key(self, key: str) -> Union[Key, str]:
        """Resolves key string to pynput Key or character."""
        return self.special_keys.get(key.lower(), key)

    def log(self, action: str) -> None:
        """Logs action string to control_log.txt with current timestamp."""
        try:
            with open("control_log.txt", "a", encoding="utf-8") as f:
                f.write(f"{datetime.now()}: {action}\n")
        except Exception as e:
            print(f"Logging error: {e}")

    def activate(self, token: Optional[str] = None) -> None:
        """Activates controller if correct authentication token is provided."""
        if token != "my_secret_token":
            self.log("Activation attempt failed.")
            return
        self.active = True
        self.activation_time = time.time()
        self.log("Controller auto-activated.")

    def deactivate(self) -> None:
        """Deactivates controller."""
        self.active = False
        self.log("Controller auto-deactivated.")

    def is_active(self) -> bool:
        """Checks if controller is currently active and within expiry timeout (300s)."""
        if not self.active:
            return False
        if self.activation_time and (time.time() - self.activation_time > 300):
            self.deactivate()
            return False
        return self.active

    async def move_cursor(self, direction: str, distance: int = 100) -> str:
        """Moves cursor in a specified direction by distance in pixels (clamped 1-2000px)."""
        if not self.is_active():
            return "🛑 Controller is inactive."
        distance = max(1, min(distance, 2000))
        x, y = self.mouse.position
        if direction == "left":
            self.mouse.position = (x - distance, y)
        elif direction == "right":
            self.mouse.position = (x + distance, y)
        elif direction == "up":
            self.mouse.position = (x, y - distance)
        elif direction == "down":
            self.mouse.position = (x, y + distance)
        else:
            return f"❌ Invalid direction: {direction}"
        await asyncio.sleep(0.2)
        self.log(f"Mouse moved {direction} by {distance}px")
        return f"🖱️ Moved mouse {direction} by {distance}px."

    async def mouse_click(self, button: str = "left") -> str:
        """Performs mouse click (left, right, middle, or double)."""
        if not self.is_active():
            return "🛑 Controller is inactive."
        btn_clean = button.lower().strip()
        if btn_clean == "left":
            self.mouse.click(Button.left, 1)
        elif btn_clean == "right":
            self.mouse.click(Button.right, 1)
        elif btn_clean == "middle":
            self.mouse.click(Button.middle, 1)
        elif btn_clean == "double":
            self.mouse.click(Button.left, 2)
        else:
            return f"❌ Invalid mouse button: {button}"
        await asyncio.sleep(0.2)
        self.log(f"Mouse clicked: {btn_clean}")
        return f"🖱️ {btn_clean.capitalize()} click."

    async def scroll_cursor(self, direction: str, amount: int = 10) -> str:
        """Scrolls cursor up or down."""
        if not self.is_active():
            return "🛑 Controller is inactive."
        amount = max(1, min(amount, 100))
        try:
            if direction == "up":
                self.mouse.scroll(0, amount)
            elif direction == "down":
                self.mouse.scroll(0, -amount)
            else:
                return f"❌ Invalid scroll direction: {direction}"
        except Exception:
            pyautogui.scroll(amount * 100 if direction == "up" else -amount * 100)
        await asyncio.sleep(0.2)
        self.log(f"Mouse scrolled {direction}")
        return f"🖱️ Scrolled {direction}"

    async def type_text(self, text: str) -> str:
        """Types string text character by character."""
        if not self.is_active():
            return "🛑 Controller is inactive."
        if not text:
            return "❌ No text provided to type."
        for char in text:
            if not char.isprintable():
                continue
            try:
                self.keyboard.press(char)
                self.keyboard.release(char)
                await asyncio.sleep(0.05)
            except Exception:
                continue
        self.log(f"Typed text: {text}")
        return f"⌨️ Typed: {text}"

    async def press_key(self, key: str) -> str:
        """Presses and releases a single valid key."""
        if not self.is_active():
            return "🛑 Controller is inactive."
        if key.lower() not in self.special_keys and key.lower() not in self.valid_keys:
            return f"❌ Invalid key: {key}"
        k = self.resolve_key(key)
        try:
            self.keyboard.press(k)
            self.keyboard.release(k)
        except Exception as e:
            return f"❌ Failed key: {key} — {e}"
        await asyncio.sleep(0.2)
        self.log(f"Pressed key: {key}")
        return f"⌨️ Key '{key}' pressed."

    async def press_hotkey(self, keys: List[str]) -> str:
        """Presses and releases a key combination."""
        if not self.is_active():
            return "🛑 Controller is inactive."
        if not keys:
            return "❌ No hotkey combination provided."
        resolved = []
        for k in keys:
            if k.lower() not in self.special_keys and k.lower() not in self.valid_keys:
                return f"❌ Invalid key in hotkey: {k}"
            resolved.append(self.resolve_key(k))

        for k in resolved:
            self.keyboard.press(k)
        for k in reversed(resolved):
            self.keyboard.release(k)
        await asyncio.sleep(0.3)
        self.log(f"Pressed hotkey: {' + '.join(keys)}")
        return f"⌨️ Hotkey {' + '.join(keys)} pressed."

    async def control_volume(self, action: str) -> str:
        """Controls system audio volume (up, down, mute)."""
        if not self.is_active():
            return "🛑 Controller is inactive."
        act_clean = action.lower().strip()
        if act_clean == "up":
            pyautogui.press("volumeup")
        elif act_clean == "down":
            pyautogui.press("volumedown")
        elif act_clean == "mute":
            pyautogui.press("volumemute")
        else:
            return f"❌ Invalid volume action: {action}"
        await asyncio.sleep(0.2)
        self.log(f"Volume control: {act_clean}")
        return f"🔊 Volume {act_clean}."

    async def swipe_gesture(self, direction: str) -> str:
        """Executes mouse drag swipe gesture in a direction."""
        if not self.is_active():
            return "🛑 Controller is inactive."
        try:
            screen_width, screen_height = pyautogui.size()
            x, y = screen_width // 2, screen_height // 2
            if direction == "up":
                pyautogui.moveTo(x, y + 200)
                pyautogui.dragTo(x, y - 200, duration=0.5)
            elif direction == "down":
                pyautogui.moveTo(x, y - 200)
                pyautogui.dragTo(x, y + 200, duration=0.5)
            elif direction == "left":
                pyautogui.moveTo(x + 200, y)
                pyautogui.dragTo(x - 200, y, duration=0.5)
            elif direction == "right":
                pyautogui.moveTo(x - 200, y)
                pyautogui.dragTo(x + 200, y, duration=0.5)
            else:
                return f"❌ Invalid swipe direction: {direction}"
        except Exception as e:
            self.log(f"Swipe gesture error: {e}")
            return f"❌ Swipe gesture failed: {e}"
        await asyncio.sleep(0.5)
        self.log(f"Swipe gesture: {direction}")
        return f"🖱️ Swipe {direction} done."

# ------------------------------
# LiveKit Tool Wrappers Section
# ------------------------------

controller = SafeController()

async def with_temporary_activation(fn, *args, **kwargs):
    print(f"🔍 TEMP ACTIVATION: {fn.__name__} | args: {args}")
    controller.activate("my_secret_token")
    result = await fn(*args, **kwargs)
    await asyncio.sleep(2)
    controller.deactivate()
    return result

@function_tool
async def move_cursor_tool(direction: str, distance: int = 100):
    """Tool to move mouse cursor directionally."""
    return await with_temporary_activation(controller.move_cursor, direction, distance)

@function_tool
async def mouse_click_tool(button: str = "left"):
    """Tool to perform mouse click."""
    return await with_temporary_activation(controller.mouse_click, button)

@function_tool
async def scroll_cursor_tool(direction: str, amount: int = 10):
    """Tool to scroll window contents."""
    return await with_temporary_activation(controller.scroll_cursor, direction, amount)

@function_tool
async def type_text_tool(text: str):
    """Tool to type a given text sequence."""
    return await with_temporary_activation(controller.type_text, text)

@function_tool
async def press_key_tool(key: str):
    """Tool to press a specific key."""
    return await with_temporary_activation(controller.press_key, key)

@function_tool
async def press_hotkey_tool(keys: List[str]):
    """Tool to execute keyboard shortcut/hotkey combinations."""
    return await with_temporary_activation(controller.press_hotkey, keys)

@function_tool
async def control_volume_tool(action: str):
    """Tool to change system volume level or mute."""
    return await with_temporary_activation(controller.control_volume, action)

@function_tool
async def swipe_gesture_tool(direction: str):
    """Tool to perform screen drag/swipe gesture."""
    return await with_temporary_activation(controller.swipe_gesture, direction)

