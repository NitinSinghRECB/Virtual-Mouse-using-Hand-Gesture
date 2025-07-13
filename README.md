# Virtual-Mouse-using-Hand-Gesture
#  Virtual Mouse using Hand Gesture

This is a Python project that lets you control your computer mouse using hand gestures detected by webcam. It uses MediaPipe for hand tracking and OpenCV to access the camera. With this, you can move the mouse and perform click actions just using your fingers!

---

##  How It Works

- It detects hand landmarks (like fingertips and joints) using **MediaPipe**.
- Based on which fingers are up:
  - One finger up → move the cursor
  - Two fingers up → click
- It maps your finger position from webcam to screen coordinates using **autopy**.
- A smoothing technique is used to avoid sudden jumps of the mouse.

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Autopy

---

##  How to Run

### Step 1: Clone the repo
```bash
git clone https://github.com/your-username/virtual-mouse.git
cd virtual-mouse

