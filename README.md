# ⚡ PINUX: Asynchronous Smart Home Architecture

PINUX is an advanced, 8-channel asynchronous Smart Home System designed to bridge the gap between high-level cloud architecture and bare-metal ESP32 hardware. Engineered with a focus on low-latency execution and premium aesthetics, PINUX handles concurrent database synchronization, environmental weather polling, and precision timer mechanics without interrupting the core execution flow.

![PINUX UI](https://raw.githubusercontent.com/priyanshu643/PINUX/main/frontend/ui_preview.png) *(Note: Replace with your actual screenshot URL after uploading)*

---

## 🚀 Key Features

*   **Asynchronous Core:** Non-blocking Python backend and ESP32 stream-based listening for near-instant response times.
*   **Apple-Inspired UI:** A stunning "Glassmorphic" Command Center built with Vanilla JavaScript, CSS Grid, and backdrop filters.
*   **Dual-SSID Redundancy:** Automatic network fallback to ensure your home remains smart even if your primary router fails.
*   **Time-Travel Logic:** Precision timer mechanics calculated via epoch timestamps in Python to prevent "ghosting" or missed cycles.
*   **Environmental Awareness:** Real-time weather polling via Open-Meteo API to integrate outdoor conditions into your home dashboard.

---

## 🛠️ The Tech Stack

### The View (Frontend)
*   **HTML5 / CSS3:** Utilizing CSS variables, cubic-bezier animations, and Flexbox/Grid.
*   **Vanilla JS (ES6+):** Fetch API for REST communication and IntersectionObserver for fluid UI transitions.

### The Brain (Backend)
*   **Python 3:** Continuous, non-blocking service for logic processing and API orchestration.
*   **Firebase RTDB:** NoSQL central nervous system for real-time state synchronization.

### The Muscle (Hardware)
*   **ESP32:** Dual-core microcontroller handling WiFi and physical GPIO states.
*   **8-Channel Relay:** Active-LOW industrial-grade relay module for physical device control.

---

## 🗺️ System Topology

1.  **Web UI** → User sets a timer or toggles a switch.
2.  **Firebase (/devices)** → UI sends a `PATCH` request with the new state.
3.  **Python Brain** → Detects the change, calculates expiration, and updates the hardware stream.
4.  **Firebase (/payload)** → Lightweight electrical states are pushed down.
5.  **ESP32** → Receives a real-time stream event and triggers `digitalWrite()` instantly.

---

## 📂 Project Structure

```text
PINUX/
├── backend/            # Python orchestration scripts
├── firmware/           # ESP32 C++ (Arduino) source code
├── frontend/           # HTML/CSS/JS Command Center
└── documentation/      # PDF Engineering Manual & Diagrams
```

---

## ⚙️ Quick Start

1.  **Hardware:** Flash the `.ino` file to your ESP32. Ensure your relay pins match the mapping in the code (GPIO 13, 19, 14, etc.).
2.  **Firebase:** Create a Realtime Database and update the `DATABASE_URL` in all three layers (Web, Python, ESP32).
3.  **Backend:** Run `pip install requests` and start `bot.py`.
4.  **Frontend:** Open `index.html` in any modern browser.

---

## 📜 License & Author

**Project Architect:** Priyanshu Raj  
**Documentation:** [Download the PINUX Engineering Manual](./PINUX_Engineering_Manual.pdf)

*Built for the future of DIY Home Automation.*
