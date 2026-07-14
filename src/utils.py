import math
from typing import Dict, List, Tuple


LANDMARK_NAMES: Dict[int, str] = {
    0: "WRIST",
    1: "THUMB_CMC",
    2: "THUMB_MCP",
    3: "THUMB_IP",
    4: "THUMB_TIP",
    5: "INDEX_MCP",
    6: "INDEX_PIP",
    7: "INDEX_DIP",
    8: "INDEX_TIP",
    9: "MIDDLE_MCP",
    10: "MIDDLE_PIP",
    11: "MIDDLE_DIP",
    12: "MIDDLE_TIP",
    13: "RING_MCP",
    14: "RING_PIP",
    15: "RING_DIP",
    16: "RING_TIP",
    17: "PINKY_MCP",
    18: "PINKY_PIP",
    19: "PINKY_DIP",
    20: "PINKY_TIP",
}

FINGER_TIP_IDS: List[int] = [4, 8, 12, 16, 20]

FINGER_DIP_IDS: List[int] = [3, 7, 11, 15, 19]

FINGER_PIP_IDS: List[int] = [2, 6, 10, 14, 18]


def calculate_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def get_handedness_color(handedness: str) -> Tuple[int, int, int]:
    from config import Config
    return Config.COLORS["LEFT_HAND"] if handedness == "Left" else Config.COLORS["RIGHT_HAND"]
