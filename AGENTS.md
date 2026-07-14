# AGENTS.md

## Project Overview
Hand tracking application using computer vision and machine learning to detect and track hand landmarks in real-time.

## Tech Stack
- Python 3.x
- OpenCV
- MediaPipe
- NumPy

## Project Structure
```
hand-tracking/
├── src/
│   ├── __init__.py
│   ├── hand_tracker.py      # Core hand tracking logic
│   ├── utils.py             # Helper utilities
│   └── visualizer.py        # Drawing and visualization
├── main.py                  # Entry point
├── config.py                # Configuration settings
├── requirements.txt
├── AGENTS.md
├── PROMPTS.md
└── DESIGN.md
```

## Conventions
- Use type hints for all function signatures
- Follow PEP 8 style guide
- Use `snake_case` for functions/variables, `PascalCase` for classes
- Write docstrings for all public functions/classes
- Keep functions focused and small (single responsibility)

## Commands
- `pip install -r requirements.txt` — Install dependencies
- `python main.py` — Run the hand tracking application
