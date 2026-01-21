"""
Subway Surfers Virtual Controller - Hand Gesture Control
Updated to use MediaPipe Tasks API (compatible with Python 3.13)
"""
import cv2
import os
import time
import math

# Suppress TensorFlow/MediaPipe warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
from pynput.keyboard import Key, Controller

# -------------------------------------------
# INITIAL SETUP
# -------------------------------------------

keyboard = Controller()

# MediaPipe Tasks API Setup
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hand_landmarker.task')
if not os.path.exists(model_path):
    print(f"Error: Model file not found at {model_path}")
    print("Please download it using:")
    print('curl -o hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task')
    exit(1)

BaseOptions = mp.tasks.BaseOptions
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
landmarker = HandLandmarker.create_from_options(options)

# Camera setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera (index 0). Trying index 1...")
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open fallback camera. Exiting.")
        exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pTime = 0
current_action = "IDLE"

# -------------------------------------------
# STATE MEMORY (PREVENT REPEAT)
# -------------------------------------------

gesture_state = {
    'left': False,
    'right': False,
    'jump': False,
    'slide': False,
    'hover': False
}

# -------------------------------------------
# LANE BOUNDARIES
# -------------------------------------------

LEFT_BOUND = 0.35
RIGHT_BOUND = 0.65

# -------------------------------------------
# HAND LANDMARK INDICES (MediaPipe)
# -------------------------------------------

THUMB_TIP = 4
THUMB_MCP = 2
INDEX_TIP = 8
INDEX_PIP = 6
MIDDLE_TIP = 12
MIDDLE_PIP = 10
RING_TIP = 16
RING_PIP = 14
PINKY_TIP = 20
PINKY_PIP = 18

FINGER_TIPS = [THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP, PINKY_TIP]
FINGER_PIPS = [THUMB_MCP, INDEX_PIP, MIDDLE_PIP, RING_PIP, PINKY_PIP]

# -------------------------------------------
# UTILITY FUNCTIONS
# -------------------------------------------

def press_and_release(key):
    keyboard.press(key)
    keyboard.release(key)

def count_extended_fingers(landmarks):
    """Count extended fingers based on landmark positions"""
    fingers = [False] * 5
    
    # Thumb - compare x positions for thumb (different orientation)
    if landmarks[THUMB_TIP].y < landmarks[THUMB_MCP].y:
        fingers[0] = True
    
    # Other fingers - tip above pip means extended
    for i in range(1, 5):
        tip = FINGER_TIPS[i]
        pip = FINGER_PIPS[i]
        if landmarks[tip].y < landmarks[pip].y:
            fingers[i] = True
    
    return fingers

def draw_lanes(img, w, h):
    lx = int(LEFT_BOUND * w)
    rx = int(RIGHT_BOUND * w)
    cv2.line(img, (lx, 0), (lx, h), (200, 200, 200), 2)
    cv2.line(img, (rx, 0), (rx, h), (200, 200, 200), 2)

def draw_landmarks(image, landmarks, w, h):
    """Draw hand landmarks on the image"""
    # Draw all landmarks
    for lm in landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        cv2.circle(image, (x, y), 4, (0, 255, 0), -1)
    
    # Draw connections
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),      # Thumb
        (0, 5), (5, 6), (6, 7), (7, 8),      # Index
        (0, 9), (9, 10), (10, 11), (11, 12), # Middle
        (0, 13), (13, 14), (14, 15), (15, 16), # Ring
        (0, 17), (17, 18), (18, 19), (19, 20), # Pinky
        (5, 9), (9, 13), (13, 17)            # Palm
    ]
    for start_idx, end_idx in connections:
        start = landmarks[start_idx]
        end = landmarks[end_idx]
        cv2.line(image, (int(start.x * w), int(start.y * h)), 
                 (int(end.x * w), int(end.y * h)), (0, 255, 0), 2)

# -------------------------------------------
# MAIN LOOP
# -------------------------------------------

print("=" * 50)
print("  Subway Surfers Virtual Controller")
print("=" * 50)
print("Controls:")
print("  🖐 Open palm      → JUMP")
print("  🤙 Thumb + Pinky  → SLIDE")
print("  ✌️ Index + Middle → HOVERBOARD")
print("  👈 Hand on left   → Move LEFT")
print("  👉 Hand on right  → Move RIGHT")
print("  Press 'Q' to quit")
print("=" * 50)

last_timestamp_ms = -1

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    h, w, _ = image.shape

    draw_lanes(image, w, h)

    # Convert to RGB for MediaPipe
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    
    # Ensure strictly increasing timestamp
    timestamp_ms = int(time.time() * 1000)
    if timestamp_ms <= last_timestamp_ms:
        timestamp_ms = last_timestamp_ms + 1
    last_timestamp_ms = timestamp_ms
    
    # Run hand detection
    results = landmarker.detect_for_video(mp_image, timestamp_ms)

    current_action = "IDLE"

    if results.hand_landmarks:
        landmarks = results.hand_landmarks[0]
        
        # Get thumb and index positions for lane detection
        thumb = landmarks[THUMB_TIP]
        index = landmarks[INDEX_TIP]
        center_x = (thumb.x + index.x) / 2

        fingers = count_extended_fingers(landmarks)

        # Draw landmarks
        draw_landmarks(image, landmarks, w, h)

        # -----------------------------
        # JUMP → OPEN PALM
        # -----------------------------
        if all(fingers):
            if not gesture_state['jump']:
                press_and_release(Key.up)
                gesture_state['jump'] = True
            current_action = "JUMP"
        else:
            gesture_state['jump'] = False

        # -----------------------------
        # SLIDE → THUMB + PINKY
        # -----------------------------
        if fingers[0] and fingers[4] and not fingers[1] and not fingers[2] and not fingers[3]:
            if not gesture_state['slide']:
                press_and_release(Key.down)
                gesture_state['slide'] = True
            current_action = "SLIDE"
        else:
            gesture_state['slide'] = False

        # -----------------------------
        # HOVERBOARD → ✌️ INDEX + MIDDLE
        # -----------------------------
        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            if not gesture_state['hover']:
                press_and_release(Key.space)
                gesture_state['hover'] = True
            current_action = "HOVERBOARD"
        else:
            gesture_state['hover'] = False

        # -----------------------------
        # LEFT / RIGHT → HAND POSITION
        # -----------------------------
        if center_x < LEFT_BOUND:
            if not gesture_state['left']:
                press_and_release(Key.left)
                gesture_state['left'] = True
            gesture_state['right'] = False
            current_action = "LEFT"

        elif center_x > RIGHT_BOUND:
            if not gesture_state['right']:
                press_and_release(Key.right)
                gesture_state['right'] = True
            gesture_state['left'] = False
            current_action = "RIGHT"

        else:
            gesture_state['left'] = False
            gesture_state['right'] = False
            if current_action == "IDLE":
                current_action = "CENTER"

        # DEBUG - show finger states
        cv2.putText(image, f"Fingers: {fingers}", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # FPS calculation
    cTime = time.time()
    fps = int(1 / (cTime - pTime)) if cTime != pTime else 0
    pTime = cTime

    cv2.putText(image, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.putText(image, f"Action: {current_action}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Subway Surfers Virtual Controller", image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
landmarker.close()
cv2.destroyAllWindows()
