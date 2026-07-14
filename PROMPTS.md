# PROMPTS.md

## Initial Setup Prompts

### Project Scaffolding
"Create the project structure for a hand tracking application with OpenCV and MediaPipe."

### Core Implementation
"Implement the `HandTracker` class that uses MediaPipe to detect hand landmarks from a video frame. Include methods for:
- `find_hands(frame)` — Processes frame and returns results
- `find_position(frame, hand_no=0)` — Returns landmark positions for a specific hand
- `find_distance(p1, p2)` — Calculates distance between two landmarks"

### Visualization
"Create a `Visualizer` class that draws hand landmarks, connections, and bounding boxes on the frame using OpenCV drawing functions."

### Entry Point
"Write a `main.py` that captures webcam video, runs the hand tracker on each frame, and displays the annotated output in real-time. Include a 'q' key to quit."

## Future Enhancement Prompts

### Gesture Recognition
"Add gesture recognition to the hand tracker: detect gestures like thumbs up, peace sign, fist, open palm, and pointing."

### Fingertip Detection
"Implement fingertip detection by checking which landmark points correspond to the tip of each finger based on MediaPipe's 21-point landmark model."

### Mouse Control
"Use hand tracking to control the mouse cursor — map the index fingertip position to screen coordinates and trigger clicks with gestures."

### Volume Control
"Control system volume using hand gestures — map the distance between thumb and index finger to volume level."

### Smoothing & Filtering
"Add temporal smoothing using exponential moving average to reduce jitter in landmark positions."
