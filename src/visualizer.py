import time
from typing import Dict, List

import cv2
import mediapipe as mp
import numpy as np

from config import Config
from src.utils import get_handedness_color


class Visualizer:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.connections = mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS
        self.prev_time: float = 0.0

    def draw_landmarks(
        self,
        frame: np.ndarray,
        landmarks: List[Dict],
        handedness: str,
        draw_indices: bool = True,
    ) -> np.ndarray:
        color = get_handedness_color(handedness)

        for conn in self.connections:
            start_idx, end_idx = conn.start, conn.end
            if start_idx < len(landmarks) and end_idx < len(landmarks):
                pt1 = (landmarks[start_idx]["x"], landmarks[start_idx]["y"])
                pt2 = (landmarks[end_idx]["x"], landmarks[end_idx]["y"])
                cv2.line(frame, pt1, pt2, color, self.config.CONNECTION_THICKNESS)

        for lm in landmarks:
            cx, cy = lm["x"], lm["y"]
            cv2.circle(frame, (cx, cy), self.config.CIRCLE_RADIUS, color, cv2.FILLED)
            cv2.circle(
                frame,
                (cx, cy),
                self.config.CIRCLE_RADIUS,
                self.config.COLORS["CONNECTION"],
                self.config.CIRCLE_THICKNESS,
            )

            if draw_indices:
                cv2.putText(
                    frame,
                    str(lm["id"]),
                    (cx + 8, cy - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    self.config.FONT_SCALE,
                    self.config.COLORS["LANDMARK_NUMBER"],
                    self.config.FONT_THICKNESS,
                )

        return frame

    def draw_bounding_box(
        self,
        frame: np.ndarray,
        landmarks: List[Dict],
        handedness: str,
    ) -> np.ndarray:
        color = get_handedness_color(handedness)
        xs = [lm["x"] for lm in landmarks]
        ys = [lm["y"] for lm in landmarks]

        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        pad = self.config.BBOX_PADDING

        x1 = max(0, x_min - pad)
        y1 = max(0, y_min - pad)
        x2 = min(frame.shape[1], x_max + pad)
        y2 = min(frame.shape[0], y_max + pad)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, self.config.BBOX_THICKNESS)

        label = f"{handedness} Hand"
        label_y = y1 - 10 if y1 - 10 > 10 else y1 + 20
        cv2.putText(
            frame,
            label,
            (x1, label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.config.FONT_SCALE + 0.2,
            self.config.COLORS["LABEL"],
            self.config.FONT_THICKNESS + 1,
        )

        return frame

    def draw_fps(self, frame: np.ndarray) -> np.ndarray:
        curr_time = time.time()
        fps = 1.0 / (curr_time - self.prev_time) if self.prev_time > 0 else 0.0
        self.prev_time = curr_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            self.config.COLORS["FPS"],
            2,
        )
        return frame

    def draw_hand(
        self,
        frame: np.ndarray,
        landmarks: List[Dict],
        handedness: str,
        draw_bbox: bool = True,
        draw_indices: bool = True,
    ) -> np.ndarray:
        frame = self.draw_landmarks(frame, landmarks, handedness, draw_indices)
        if draw_bbox:
            frame = self.draw_bounding_box(frame, landmarks, handedness)
        return frame
