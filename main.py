import time

import cv2

from config import Config
from src.hand_tracker import HandTracker
from src.visualizer import Visualizer


def find_camera(config: Config) -> int:
    pref_id = config.CAMERA_ID

    for cam_id in [pref_id, 0, 1, 2, 3, 4, 5]:
        for backend in [cv2.CAP_MSMF, cv2.CAP_DSHOW]:
            cap = cv2.VideoCapture(cam_id, backend)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None and frame.size > 0:
                    print(f"Camera {cam_id} (backend {backend}) — {frame.shape[1]}x{frame.shape[0]}", flush=True)
                    return cam_id
    return -1


def main() -> None:
    config = Config()

    print("Scanning for cameras...", flush=True)
    cam_id = find_camera(config)
    if cam_id < 0:
        print("Error: No camera found.", flush=True)
        return

    cap = cv2.VideoCapture(cam_id, cv2.CAP_MSMF)
    if not cap.isOpened():
        print(f"Error: Could not open camera {cam_id}.", flush=True)
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, config.FPS)

    tracker = HandTracker(config)
    visualizer = Visualizer(config)

    print("Hand Tracking started. Press 'q' in the window to quit.", flush=True)

    frame_count = 0
    while True:
        success, frame = cap.read()
        if not success or frame is None:
            time.sleep(0.1)
            continue

        frame_count += 1
        if frame_count % 30 == 0:
            print(f"  Running... frame {frame_count}", flush=True)

        frame = cv2.flip(frame, 1)
        frame = tracker.find_hands(frame)

        hands_data = tracker.get_all_hands_position(frame)
        for _, landmarks, handedness in hands_data:
            frame = visualizer.draw_hand(frame, landmarks, handedness)

        frame = visualizer.draw_fps(frame)

        cv2.imshow("Hand Tracking", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Quit key pressed.", flush=True)
            break

    cap.release()
    cv2.destroyAllWindows()
    tracker.close()
    print("Hand Tracking stopped.", flush=True)


if __name__ == "__main__":
    main()
