# Opticloak
**🧥 Invisible Cloak using OpenCV**

Developed by: Neeyati Vijjeswarapu

**📌 Project Description**
This project implements a fun and fascinating Invisible Cloak effect using Python and OpenCV. It simulates invisibility by masking a specific color (like red) in real-time video and replacing it with the background image, creating the illusion of invisibility — just like in Harry Potter!

**🎯 Features**
- Real-time video processing using OpenCV
- Background capture for seamless cloak masking
- Custom color detection and masking using HSV color space
- Works with webcam
- Beginner-friendly and educational project in computer vision

**🛠️ Tech Stack**

- Python
- OpenCV
- NumPy

**📷 How It Works**

- The background is captured for a few seconds.
- The cloak (of a specific color, e.g., blue) is detected using HSV color masking.
- Pixels of the cloak are replaced with corresponding background pixels.
- The effect is displayed in real-time on webcam feed.

**🚀 Getting Started**
1. 📦 Installation

> pip install opencv-python numpy

2. ▶️ Run the Project

> python harry2.py

⚠️ Make sure you're using a blue (or the color you coded) cloth and have a plain background.

**📁 File Structure**

├── harry2.py

├── README.md

**📚 Learning Goals**
- Understanding of image masking and bitwise operations
- HSV color space in OpenCV
- Real-time webcam frame manipulation

**✅ To Do**
 - Add GUI with streamlit or tkinter
 - Support multiple cloak colors
 - Record invisibility effect
