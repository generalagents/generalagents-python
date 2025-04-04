from dataclasses import dataclass
from typing import Literal, TypeAlias


@dataclass
class Coordinate:
    """Represents a point on the screen with x and y coordinates."""

    x: int
    y: int


# Based on: https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys,
# fmt: off
KeyboardKey: TypeAlias = Literal[
    '\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')',
    '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
    'browserback', 'browserfavorites', 'browserforward', 'browserhome',
    'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
    'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
    'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
    'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
    'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
    'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
    'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
    'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
    'command', 'option', 'optionleft', 'optionright'
]
# fmt: on


ActionKind: TypeAlias = Literal[
    "key_press",
    "type",
    "left_click",
    "right_click",
    "double_click",
    "triple_click",
    "mouse_move",
    "drag",
    "scroll",
    "wait",
    "stop",
]


@dataclass
class ActionKeyPress:
    """Represents pressing one or more keyboard keys simultaneously."""

    kind: Literal["key_press"]
    keys: list[KeyboardKey]


@dataclass
class ActionType:
    """Represents typing a sequence of characters."""

    kind: Literal["type"]
    text: str


@dataclass
class ActionLeftClick:
    """Represents a left mouse button click at a specific coordinate."""

    kind: Literal["left_click"]
    coordinate: Coordinate


@dataclass
class ActionRightClick:
    """Represents a right mouse button click at a specific coordinate."""

    kind: Literal["right_click"]
    coordinate: Coordinate


@dataclass
class ActionDoubleClick:
    """Represents a double click with the left mouse button at a specific coordinate."""

    kind: Literal["double_click"]
    coordinate: Coordinate


@dataclass
class ActionTripleClick:
    """Represents a triple click with the left mouse button at a specific coordinate."""

    kind: Literal["triple_click"]
    coordinate: Coordinate


@dataclass
class ActionMouseMove:
    """Represents moving the mouse cursor to a specific coordinate without clicking."""

    kind: Literal["mouse_move"]
    coordinate: Coordinate


@dataclass
class ActionDrag:
    """Represents dragging the mouse from one coordinate to another while holding the left button."""

    kind: Literal["drag"]
    drag_start: Coordinate
    drag_end: Coordinate


@dataclass
class ActionScroll:
    """Represents scrolling the mouse wheel at a specific coordinate with the given delta."""

    kind: Literal["scroll"]
    scroll_delta: int
    coordinate: Coordinate


@dataclass
class ActionWait:
    """Represents a pause in execution to wait for UI changes or animations."""

    kind: Literal["wait"]


@dataclass
class ActionStop:
    """Represents stopping or completing the current task sequence."""

    kind: Literal["stop"]


Action: TypeAlias = (
    ActionKeyPress
    | ActionType
    | ActionLeftClick
    | ActionRightClick
    | ActionDoubleClick
    | ActionTripleClick
    | ActionMouseMove
    | ActionDrag
    | ActionScroll
    | ActionWait
    | ActionStop
)
