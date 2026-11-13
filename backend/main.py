import cv2
import pickle
import cvzone
import numpy as np
import json
from flask import Flask, render_template, Response
import time

app = Flask(__name__)

# Video feed setup
cap = cv2.VideoCapture('./frontend/assets/media/park_video.mp4')


fps = cap.get(cv2.CAP_PROP_FPS)
if fps > 0:
    frame_delay = 1 / fps
else:
    frame_delay = 0.03
    print("Warning: FPS is zero. Using default delay.")



# Load parking positions
import pickle
with open('backend/CarParkPos', 'rb') as file:
    posList = pickle.load(file)
print(posList)

# Set dimensions for each parking spot
width, height = 70, 34

# Function to update parking status and draw rectangles
def generate_frames():
    last_frame_time = time.time()
    while True:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        success, img = cap.read()
        if not success:
            break

        # Process image for parking status detection
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        # Draw rectangles for parking slots
        spaceCounter = 0
        for pos in posList:
            x, y = pos
            imgCrop = imgDilate[y:y + height, x:x + width]
            count = cv2.countNonZero(imgCrop)
            color = (0, 255, 0) if count < 350 else (0, 0, 255)
            thickness = 5 if count < 350 else 2
            spaceCounter += 1 if count < 350 else 0
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1, thickness=2, offset=0, colorR=color)
        
        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (140, 20), scale=1.5, thickness=2, offset=10, colorR=(0, 200, 0))

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        # Maintain a consistent frame rate for the HTML display
        current_time = time.time()
        elapsed_time = current_time - last_frame_time
        if elapsed_time < frame_delay:
            time.sleep(frame_delay - elapsed_time)
        last_frame_time = time.time()

        # Yield the frame to the HTML stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')