from __future__ import annotations
import time
from typing import Tuple
import pyautogui

def setup_pyautogui(failsafe: bool = True, pause: float = 0.2) -> None:
    pyautogui.FAILSAFE = failsafe
    pyautogui.PAUSE = pause

def click_point(point: Tuple[int, int], clicks: int = 1, interval: float = 0.05) -> None:
    x, y = point
    pyautogui.click(x=x, y=y, clicks=clicks, interval=interval)

def type_text(text: str, interval: float = 0.01) -> None:
    pyautogui.typewrite(text, interval=interval)

def press(key: str) -> None:
    pyautogui.press(key)

def hotkey(*keys: str) -> None:
    pyautogui.hotkey(*keys)

def wait(seconds: float) -> None:
    time.sleep(seconds)

def screenshot(path: str) -> None:
    pyautogui.screenshot(path)
