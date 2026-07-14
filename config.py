import os
from typing import Dict, Tuple


class Config:
    MODEL_PATH: str = os.path.join(
        os.path.dirname(__file__), "models", "hand_landmarker.task"
    )
    CAMERA_ID: int = 0
    FRAME_WIDTH: int = 640
    FRAME_HEIGHT: int = 480
    FPS: int = 30

    MAX_HANDS: int = 2
    DETECTION_CONFIDENCE: float = 0.7
    TRACKING_CONFIDENCE: float = 0.5

    COLORS: Dict[str, Tuple[int, int, int]] = {
        "LEFT_HAND": (255, 0, 0),
        "RIGHT_HAND": (0, 0, 255),
        "CONNECTION": (255, 255, 255),
        "LABEL": (255, 255, 255),
        "FPS": (0, 255, 0),
        "LANDMARK_NUMBER": (255, 255, 255),
    }

    FONT = None
    FONT_SCALE: float = 0.5
    FONT_THICKNESS: int = 1
    CIRCLE_RADIUS: int = 6
    CIRCLE_THICKNESS: int = 2
    BBOX_PADDING: int = 20
    BBOX_THICKNESS: int = 2
    CONNECTION_THICKNESS: int = 2
