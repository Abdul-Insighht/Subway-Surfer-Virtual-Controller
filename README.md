# 🎮 Subway Surfers Virtual Controller

A real-time **gesture-based virtual controller** for Subway Surfers built using **Computer Vision**.  
Control the game using **hand movements and gestures** — no external controllers needed!

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange?logo=google)

---

## 🎬 Demo

![Demo](Demo.gif.gif)

---

## 🚀 Features

| Gesture | Action |
|---------|--------|
| 🖐 **Open Palm** (all fingers extended) | **Jump** |
| 🤙 **Thumb + Pinky** only | **Slide** |
| ✌️ **Index + Middle** only | **Hoverboard** |
| 👈 **Hand on left side** | Move **Left** |
| 👉 **Hand on right side** | Move **Right** |

- 📊 Live FPS & action display
- 🧠 Stable, rule-based gesture logic
- 🎯 Uses MediaPipe Tasks API (Python 3.13 compatible)

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **OpenCV** | Camera capture & image processing |
| **MediaPipe** | Real-time hand landmark detection |
| **Pynput** | Keyboard simulation |

---

## ⚙️ How It Works

1. **MediaPipe** detects hand landmarks in real-time
2. **Hand position** determines left/right lane movement
3. **Finger combinations** trigger jump, slide & hoverboard
4. **Keyboard inputs** are simulated using `pynput`

This approach focuses on **stability, low latency, and simplicity**, making it suitable for real-time gameplay.

---

## 📦 Installation

### Prerequisites

- Python 3.9 - 3.13
- A webcam

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abdul-Insighht/Subway-Surfer-Virtual-Controller.git
   cd Subway-Surfer-Virtual-Controller
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the MediaPipe Hand Landmarker model:**
   ```bash
   curl -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
   ```

   Or on Windows PowerShell:
   ```powershell
   Invoke-WebRequest -Uri "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" -OutFile "hand_landmarker.task"
   ```

4. **Run the controller:**
   ```bash
   cd "Subway-Surfer Virtual Controller"
   python Virtual_controller.py
   ```

5. **Start Subway Surfers** and enjoy gesture control!

---

## 🕹️ Usage Tips

- Position your hand in front of the camera
- Keep your hand within the frame
- Use a well-lit environment for best detection
- Press **Q** to quit the controller

---

## 📁 Project Structure

```
Subway-Surfer-Virtual-Controller/
├── Subway-Surfer Virtual Controller/
│   └── Virtual_controller.py    # Main controller script
├── hand_landmarker.task          # MediaPipe hand tracking model
├── Demo.gif.gif                  # Demo animation
├── requirements.txt              # Python dependencies
├── LICENSE
└── README.md
```

---

## ⚠️ Notes

- **Python 3.13 Compatible**: Uses the modern MediaPipe Tasks API
- **Camera Access**: Ensure your webcam is not used by other apps
- **Permissions**: On some systems, pynput may require admin privileges

---

## 📬 Contact

**Hafiz Abdul Rehman**

- 📧 Email: [hafizrehman3321@gmail.com](mailto:hafizrehman3321@gmail.com)
- 💼 LinkedIn: [Hafiz Abdul Rehman](https://linkedin.com/in/hafiz-abdul-rehman-9990ab329)
- 🐙 GitHub: [Abdul-Insighht](https://github.com/Abdul-Insighht)

---

## 🌟 Show Your Support

If you find this project helpful, please consider:

- ⭐ **Starring** this repository
- 🔄 **Sharing** with others
- 🐛 **Reporting** issues
- 💡 **Suggesting** improvements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ by <b>Hafiz Abdul Rehman</b></p>
