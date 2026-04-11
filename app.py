import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.title("Zero Touch Pad (Gesture Control)")

st.write("Turn on camera and try gestures")

run = st.checkbox("Start Camera")

FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

mp_draw = mp.solutions.drawing_utils

def get_finger_states(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # thumb
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # other fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

while run:
    success, frame = cap.read()
    if not success:
        st.write("Camera not working")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    gesture_text = "No Gesture"

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            fingers = get_finger_states(handLms)

            # Gesture logic
            if fingers == [0,1,0,0,0]:
                gesture_text = "Move Cursor (Index Finger)"

            elif fingers == [0,1,1,0,0]:
                gesture_text = "Scroll Gesture"

            elif fingers == [1,1,0,0,0]:
                gesture_text = "Click Gesture"

            elif fingers == [0,1,1,1,1]:
                gesture_text = "Open Palm"

            elif fingers == [0,0,0,0,0]:
                gesture_text = "Fist (Drag)"

    cv2.putText(frame, gesture_text, (10,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    FRAME_WINDOW.image(frame)

cap.release()
