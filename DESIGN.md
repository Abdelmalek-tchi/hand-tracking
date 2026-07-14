# DESIGN.md

## Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  main.py    │────▶│ HandTracker  │────▶│  Visualizer  │
│ (Pipeline)  │     │ (Detection)  │     │ (Drawing)    │
└─────────────┘     └──────────────┘     └──────────────┘
       │                                         │
       │                                         ▼
       │                                  ┌──────────────┐
       └──────────────────────────────────│   Viewer     │
                                          │ (OpenCV GUI) │
                                          └──────────────┘
```

## Components

### 1. HandTracker (`src/hand_tracker.py`)
- Wraps MediaPipe Hands solution
- Processes BGR frames from OpenCV
- Returns normalized landmark coordinates
- Configurable: detection confidence, tracking confidence, max hands

### 2. Visualizer (`src/visualizer.py`)
- Draws landmarks and connections using MediaPipe drawing specs
- Draws bounding boxes around detected hands
- Annotates landmark indices on request
- Color-coded for left vs right hand

### 3. main.py
- Captures webcam feed via OpenCV `VideoCapture`
- Loops: read frame → detect → visualize → display
- Exits on 'q' key press
- Handles window cleanup

### 4. config.py
Central configuration:
```python
CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS = 30
MAX_HANDS = 2
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.5
```

## Data Flow
1. Webcam → BGR frame → HandTracker
2. HandTracker → MediaPipe → landmarks (x, y, z)
3. Visualizer → annotated frame overlay
4. Annotated frame → OpenCV imshow window

## Landmark Model (MediaPipe)
21 landmarks per hand:
- 0: Wrist
- 1-4: Thumb (CMC, MCP, IP, TIP)
- 5-8: Index (MCP, PIP, DIP, TIP)
- 9-12: Middle (MCP, PIP, DIP, TIP)
- 13-16: Ring (MCP, PIP, DIP, TIP)
- 17-20: Pinky (MCP, PIP, DIP, TIP)

## Future Considerations
- Add gesture classification module
- Add coordinate transformation for screen mapping
- Support for multiple camera sources
- Performance optimizations (frame skipping, ROI cropping)
