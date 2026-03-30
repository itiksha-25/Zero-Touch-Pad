# Zero-Touch-Pad
A small fully functional easy app which helps use the laptop or device without any touch. It is touch free. It has a bunch of features and can be used for any device with a working canmera in good light.

## Overview

This project uses computer camera to see and track hand gestures and change them into the needed actions on the system.
It let's us do interactions with the computer without any touch, which makes it useful in situations where user cannot touch the laptop or device.

The system sees hand movements and finger positions currently and maps them to actions like cursor movement, clicking, scrolling, and system controls.

## Features
1. Cursor Control -> Index finger
2. Left click -> Index + Thumb touch
3. RIght Click -> Middle + Thumb touch
4. Show Desktop -> Palm DWn
5. Close App -> Make fist for 3 seconds
6. Volume -> Distance between Thumb and Little finger
7. Scroll -> First 2 fingers up or down
8. Drag -> long left click
9. Screenchot -> First 3 fingers up
----
## Technologies Used

1. Python 3.10 : Core programming language
2. OpenCV (cv2) : Camera handling and image processing
3. MediaPipe : Hand tracking and landmark detection
4. PyAutoGUI : Controls mouse and system actions
5. Math & Time Modules :Used for gesture calculations and timing

---
## How It Works

1. The webcam captures live video input
2. MediaPipe detects the hand and identifies 21 landmark points
3. The program checks which fingers are up or down
4. Based on gestures and distances between fingers, actions are triggered
5. PyAutoGUI executes these actions on the system

## How to Install and use
1. Install Python 3.10 version (does not work for updates)
2. Install all the requirements.txt libraries
   
    ````
    pip install -r requirements.txt
    ````
4. Run the Project by
   
   ````
   py -3.10 main.py
   ````

 ---

## To Test

1. Run the program and make sure camera can work
2. Keep your hand in front of the camera
3. Try all the above things one by one
4. Make sure you have good light so camera sees well
5. Click 'i' key to stop the app

---

## Limitations

1. Does not work with bad lighting
2. Accuracy may reduce with complex backgrounds
3. Needs a camera for app to work
4. Fast movement can reduce detection accuracy

---

## Future Improvements

1. Multi-hand support
2. Custom gesture mapping
3. Better accuracy
4. Better speed
5. Can be used in phone
6. Include voice
7. Include ASL

---

 ## Conclusion

This project shows how computer camera can be used to create a touch-less user interface.
It gives a practical solution for real-world problem when people cannot use touch to use the device.
