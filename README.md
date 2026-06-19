# HotspotShield-DataSaver 📉✈️

A real-time Python desktop application designed to stop background processes from stealthily consuming your mobile data while connected to a hotspot. Built with a sleek, modern UI using **CustomTkinter** and powered by **psutil** for network thread tracking.

---

## ❓ The Problem
When you connect a laptop to a mobile hotspot, the operating system often treats it as a standard unmetered Wi-Fi connection. Background tasks like telemetry, cloud synchronization (OneDrive, iCloud, Creative Cloud), and system updaters immediately trigger in the background—often draining a 1GB or 2GB mobile data plan in minutes without user intervention.

## 💡 The Solution
**HotspotShield-DataSaver** provides an instant, centralized dashboard that:
1. Automatically scans for background processes making active internet connections.
2. Calculates and updates their data consumption speeds (`KB/s` or `MB/s`) in real-time.
3. Provides a one-click **Kill Process** switch to instantly terminate background data hogs.

---

## ✨ Features
* **Real-Time Bandwidth Tracking:** Lightweight background threading maps data deltas every second.
* **Smart Unit Conversion:** Dynamically switches units between `B/s`, `KB/s`, and `MB/s` based on traffic intensity.
* **Modern UI Dashboard:** Built using CustomTkinter with support for native Dark/Light mode scaling.
* **Safe List Defaults:** Automatically filters out critical operating system processes (`System`, `svchost.exe`) to protect system stability.

---

## 🛠️ Tech Stack & Tools
* **Language:** Python 3.x
* **GUI Framework:** CustomTkinter (Tkinter extension for modern UI elements)
* **System Utilities:** `psutil` (Process and system utilities library for data/network tracking)
* **Concurrency:** Native Python `threading`

---

## 🚀 Getting Started

Follow these steps to run the project locally on your machine.

### Prerequisites
Make sure you have Python 3 installed. You can check by running:
```bash
python --version
