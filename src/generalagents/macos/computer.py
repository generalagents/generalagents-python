import subprocess
import tempfile
import time
from fractions import Fraction

import pyautogui
from PIL import Image

from generalagents.action import (
    Action,
    ActionDoubleClick,
    ActionDrag,
    ActionKeyPress,
    ActionLeftClick,
    ActionMouseMove,
    ActionRightClick,
    ActionScroll,
    ActionStop,
    ActionTripleClick,
    ActionType,
    ActionWait,
    Coordinate,
)

pyautogui.FAILSAFE = True  # Move mouse to corner to abort


class Computer:
    def __init__(self, pause_after_action: float = 0.1, pause_for_wait: float = 0.1):
        self.pause_after_action = pause_after_action
        self.pause_for_wait = pause_for_wait

        w, h = pyautogui.size()
        self.scale_factor = Fraction(max(w, h), 1200)
        self.size = (round(w / self.scale_factor), round(h / self.scale_factor))

    def observe(self) -> Image.Image:
        """Observe current state of the computer"""
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            subprocess.run(["screencapture", "-C", "-x", "-m", f.name], check=True)
            return Image.open(f.name).resize(self.size)

    def execute(self, action: Action) -> Image.Image:
        """Execute a control action and observe the resulting state of the computer."""
        self._execute_action(action)
        time.sleep(self.pause_after_action)
        return self.observe()

    def _scaled(self, coord: Coordinate) -> tuple[int, int]:
        return round(coord.x * self.scale_factor), round(coord.y * self.scale_factor)

    def _execute_action(self, action: Action) -> None:
        match action:
            case ActionKeyPress(kind="key_press", keys=keys) if keys:
                pyautogui.hotkey(*keys)

            case ActionType(kind="type", text=text) if text:
                pyautogui.write(text)

            case ActionLeftClick(kind="left_click", coordinate=coord):
                pyautogui.click(*self._scaled(coord), button="left")

            case ActionRightClick(kind="right_click", coordinate=coord):
                pyautogui.click(*self._scaled(coord), button="right")

            case ActionDoubleClick(kind="double_click", coordinate=coord):
                pyautogui.doubleClick(*self._scaled(coord))

            case ActionTripleClick(kind="triple_click", coordinate=coord):
                pyautogui.tripleClick(*self._scaled(coord))

            case ActionMouseMove(kind="mouse_move", coordinate=coord):
                pyautogui.moveTo(*self._scaled(coord))

            case ActionDrag(kind="drag", drag_start=start, drag_end=end):
                pyautogui.moveTo(*self._scaled(start))
                pyautogui.dragTo(*self._scaled(end), duration=0.5)

            case ActionScroll(kind="scroll", scroll_delta=delta):
                pyautogui.scroll(float(delta * self.scale_factor))

            case ActionWait(kind="wait"):
                pyautogui.sleep(self.pause_for_wait)

            case ActionStop(kind="stop"):
                pass
