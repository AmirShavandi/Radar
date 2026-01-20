🛰️ AI-Radar: Webcam Security & Detection System
A Python-based surveillance application that simulates a military-style radar interface while using real-time Computer Vision to detect human presence via your webcam.

🌟 Features
Real-time Face Detection: Uses Haar Cascades to identify human faces instantly.

Simulated Radar UI: A custom-drawn, rotating radar sweep that visually indicates when a target is localized.

Cross-Platform Audio Alerts: * Windows: Triggers a "wee-woo" high/low frequency siren.

macOS: Uses system-level Text-to-Speech to announce intruders.

Linux/Other: Uses the terminal bell fallback.

Smart Detection Logic: Designed to alert only once per continuous sighting to avoid "noise spam."

🛠️ Installation
1. Prerequisites

Ensure you have Python installed (3.7 or higher recommended).

2. Install Dependencies

You will need OpenCV and NumPy. Install them via terminal/command prompt:

Bash
pip install opencv-python numpy
3. Haarcascade File

The app uses the default OpenCV haarcascade_frontalface_default.xml. This is usually included with the library, but ensure your environment has access to it.

🚀 How to Use
Connect your webcam.

Run the script:

Bash
python main.py
Two Windows will appear:

CAMERA: Your live feed with red circles around detected faces.

RADAR: A graphical sweep. A red blip will appear on the radar when a person is detected.

Press 'q' on your keyboard to exit the application.
