# Touchless Presentation Controller

## Project Description

A real-time, multimodal Computer Vision application that allows users to control computer presentations (PowerPoint, Keynote, Google Slides) using hand gestures.By leveraging Google's MediaPipe for sub-millisecond 3D hand-landmark detection and translating spatial coordinates into localized system commands, this system entirely removes the need for a physical clicker.

## Key Features

- Zero-Latency Processing: Utilizes Python threading to decouple system-level key presses from the main video loop, ensuring the webcam feed remains at a smooth, locked frame-rate.
- Dynamic Heads-Up Display (HUD): Custom OpenCV UI overlays feature a real-time gesture feedback loop and a mathematically driven cooldown progress bar.
- Object-Oriented Architecture: Core AI tracking is isolated within a reusable HandTrackingModule, keeping the main application logic clean and scalable.
- Highly Configurable: Keybindings, camera indices, and cooldown timers are centralized in a configuration dictionary for rapid adaptation to different operating systems and presentation software.

## Tech Stack

- Language: Python
- Computer Vision: OpenCV (cv2)
- Machine Learning / AI: MediaPipe (mp.solutions.hands)
- System Interaction: PyAutoGUI, Threading

## Gesture Mapping

The system tracks the Y-axis differential between the fingertips and the lower knuckles to determine binary states (open/closed) for all four primary fingers.

| Gesture           | Finger State | Action            | System Key Press |
|-------------------|--------------|-------------------|------------------|
| Index Up          | [1, 0, 0, 0] | Next Slide        | Right Arrow      |
| Index & Middle Up | [1, 1, 0, 0] | Previous Slide    | Left Arrow       |
| Open Palm         | [1, 1, 1, 1] | Exit Presentation | Escape           |
| Closed Fist       | [0, 0, 0, 0] | Waiting/Idle      | None             |

## Installation & Setup

Clone the repository:

```bash
git clone https://github.com/andrewstn/touchless-presenter.git
cd touchless-presenter
```

Create a virtual environment:(Note: Python 3.10 or 3.11 is recommended for MediaPipe compatibility on Mac Apple Silicon).

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```
