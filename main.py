import cv2
import mediapipe as mp
import autopy
import numpy as np
import time
import math

# Initialize
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0

# Capture Video
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

# Get Screen Size
wScr, hScr = autopy.screen.size()

# Finger Tip IDs
tipIds = [4, 8, 12, 16, 20]

def fingersUp(lmList):
    fingers = []
    if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    lmList = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * wCam), int(lm.y * hCam)
                lmList.append([id, cx, cy])

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:] # Middle finger tip

        fingers = fingersUp(lmList)

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Move Mode (Index finger only)
        if fingers[1] == 1 and fingers[2] == 0:
            # Convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # Smoothen
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Move Mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Click Mode (Both index and middle fingers up)
        if fingers[1] == 1 and fingers[2] == 1:
            length = math.hypot(x2 - x1, y2 - y1)
            if length < 40:
                cv2.circle(img, ((x1 + x2)//2, (y1 + y2)//2), 10, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
