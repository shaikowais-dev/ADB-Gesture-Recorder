# ADB Advanced Gesture Recorder

## 🚀 Overview
ADB Advanced Gesture Recorder is a Python-based desktop tool that captures real-time touch gestures from an Android device using ADB (`getevent`) and converts them into executable ADB shell commands.

It intelligently detects:
- ✅ Tap
- ✅ Long Press
- ✅ Swipe gestures

and allows users to export them as a reusable automation script.

---

## 🛠️ Features

- 🎯 Real-time gesture recording from Android device
- 📊 Smart gesture classification (Tap / Long Press / Swipe)
- 🧠 Noise filtering for accurate movement detection
- 🧾 Generates ready-to-use ADB commands
- 💾 Export recorded steps as `.sh` script
- 🖥️ Simple Tkinter GUI interface

---

## 📦 Requirements

- Python 3.x
- Android Debug Bridge (ADB) installed and configured
- USB debugging enabled on Android device

Install ADB:
👉 https://developer.android.com/tools/adb

---

## ▶️ How to Run

```bash
python recorder.py
``

How to Use:
1. Connect your Android device via USB
2. Enable USB Debugging
3. Launch the application
4. Click Start Recording
5. Perform gestures on your device
6. Click Stop Recording
7. Click Export Script to save commands