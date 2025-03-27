import cattrs

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


def test_structure():
    dict_ = {"kind": "key_press", "keys": ["a", "b"]}
    action = ActionKeyPress(kind="key_press", keys=["a", "b"])
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionType
    dict_ = {"kind": "type", "text": "Hello, World!"}
    action = ActionType(kind="type", text="Hello, World!")
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionLeftClick
    dict_ = {"kind": "left_click", "coordinate": {"x": 100, "y": 200}}
    action = ActionLeftClick(kind="left_click", coordinate=Coordinate(x=100, y=200))
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionRightClick
    dict_ = {"kind": "right_click", "coordinate": {"x": 100, "y": 200}}
    action = ActionRightClick(kind="right_click", coordinate=Coordinate(x=100, y=200))
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionDoubleClick
    dict_ = {"kind": "double_click", "coordinate": {"x": 100, "y": 200}}
    action = ActionDoubleClick(kind="double_click", coordinate=Coordinate(x=100, y=200))
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionTripleClick
    dict_ = {"kind": "triple_click", "coordinate": {"x": 100, "y": 200}}
    action = ActionTripleClick(kind="triple_click", coordinate=Coordinate(x=100, y=200))
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionMouseMove
    dict_ = {"kind": "mouse_move", "coordinate": {"x": 100, "y": 200}}
    action = ActionMouseMove(kind="mouse_move", coordinate=Coordinate(x=100, y=200))
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionDrag
    dict_ = {
        "kind": "drag",
        "drag_start": {"x": 100, "y": 200},
        "drag_end": {"x": 300, "y": 400},
    }
    action = ActionDrag(
        kind="drag",
        drag_start=Coordinate(x=100, y=200),
        drag_end=Coordinate(x=300, y=400),
    )
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionScroll
    dict_ = {"kind": "scroll", "scroll_delta": -100}
    action = ActionScroll(kind="scroll", scroll_delta=-100)
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionWait
    dict_ = {"kind": "wait"}
    action = ActionWait(kind="wait")
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]

    # Test ActionStop
    dict_ = {"kind": "stop"}
    action = ActionStop(kind="stop")
    assert action == cattrs.structure(dict_, Action)  # pyright: ignore [reportArgumentType]
