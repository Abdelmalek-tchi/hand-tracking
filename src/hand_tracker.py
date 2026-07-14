from typing import Dict, List, Optional, Tuple

import cv2
import mediapipe as mp
import numpy as np

from config import Config


class HandTracker:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.results: Optional[mp.tasks.vision.HandLandmarkerResult] = None

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(
                model_asset_path=config.MODEL_PATH
            ),
            running_mode=mp.tasks.vision.RunningMode.IMAGE,
            num_hands=config.MAX_HANDS,
            min_hand_detection_confidence=config.DETECTION_CONFIDENCE,
            min_tracking_confidence=config.TRACKING_CONFIDENCE,
        )
        self.landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)

    def find_hands(self, frame: np.ndarray) -> np.ndarray:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        self.results = self.landmarker.detect(mp_image)
        return frame

    def find_position(
        self, hand_no: int = 0
    ) -> Tuple[bool, Optional[List[Dict]], Optional[str]]:
        if not self.results or not self.results.hand_landmarks:
            return False, None, None

        if hand_no >= len(self.results.hand_landmarks):
            return False, None, None

        landmarks_list = []
        handedness_label = None
        if hand_no < len(self.results.handedness):
            handedness_label = self.results.handedness[hand_no][0].category_name

        for idx, lm in enumerate(self.results.hand_landmarks[hand_no]):
            landmarks_list.append({
                "id": idx,
                "x": int(lm.x * 640),
                "y": int(lm.y * 480),
                "z": lm.z,
                "norm_x": lm.x,
                "norm_y": lm.y,
            })

        return True, landmarks_list, handedness_label

    def find_distance(self, p1: Dict, p2: Dict) -> Tuple[float, Tuple[int, int], Tuple[int, int]]:
        x1, y1 = p1["x"], p1["y"]
        x2, y2 = p2["x"], p2["y"]
        distance = np.linalg.norm(np.array([x1 - x2, y1 - y2]))
        return distance, (x1, y1), (x2, y2)

    def get_all_hands_position(
        self, frame: np.ndarray
    ) -> List[Tuple[int, List[Dict], str]]:
        if not self.results or not self.results.hand_landmarks:
            return []

        h, w, _ = frame.shape
        hands_data = []

        for hand_idx, landmarks in enumerate(self.results.hand_landmarks):
            landmark_list = []
            handedness = "Right"
            if hand_idx < len(self.results.handedness):
                handedness = self.results.handedness[hand_idx][0].category_name
            for idx, lm in enumerate(landmarks):
                landmark_list.append({
                    "id": idx,
                    "x": int(lm.x * w),
                    "y": int(lm.y * h),
                    "z": lm.z,
                    "norm_x": lm.x,
                    "norm_y": lm.y,
                })
            hands_data.append((hand_idx, landmark_list, handedness))

        return hands_data

    def close(self) -> None:
        self.landmarker.close()
