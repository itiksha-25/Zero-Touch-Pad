#getall lib to start this app
import cv2
import mediapipe as mp
import pyautogui
import math
import time


pyautogui.FAILSAFE = False          # to protect when mouse goes to corner 


#STRAT MEDIAPIPE HAND TRACKING
mp_hnd = mp.solutions.hands
hnd = mp_hnd.Hands(                 
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# For 21 landmarks
mp_draw = mp.solutions.drawing_utils


# scr, CAMERA go
scr_breath, scr_lenth = pyautogui.size()

cap = cv2.VideoCapture(0)       #switch camera on


# so that drag is not taken as touchs etc
kween = False
corekt_touching = False
pinch_go_time = None
fist_go_time = None
last_touch_time = 0         #very important

prev_x, prev_y = 0, 0       #initial guess
smoothening = 5              #more is good but very bad lag

current_action = "Waiting..."


# main for everything to work nicely
while True:
    success, img = cap.read()
    if not success:
        break

    # swap wring right to image
    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    # make to 3 colors for MediaPipe
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #check for hand exist in camera
    results = hnd.process(img_rgb)

    current_action = "NO HAND"


    #HAND check and 21 poinys assign 
    if results.multi_hand_landmarks:
        current_action = "NO HAND MOVEMENT"

        for hand_landmarks in results.multi_hand_landmarks:
            lms = hand_landmarks.landmark


            # check finger where- up or dowN
            index_up = lms[8].y < lms[6].y          #fist finger
            middle_up = lms[12].y < lms[10].y       #middle finger
            ring_up = lms[16].y < lms[14].y         #marriage finger
            pinky_up = lms[20].y < lms[18].y        #small finger
            thumb_up = lms[4].y < lms[3].y          #thick finger


            # close app when all finger and thumb tgthr
            if not index_up and not middle_up and not ring_up and not pinky_up:
                current_action = "FIST: Closing App..."
                if fist_go_time is None:
                    fist_go_time = time.time()

                elif time.time() - fist_go_time > 3:
                    pyautogui.hotkey('alt', 'f4')
                    time.sleep(1)
                    fist_go_time = None


            else:
                fist_go_time = None


                #for SS
                if index_up and middle_up and ring_up and not pinky_up:
                    current_action = "TTAKE SCREENSHOT"
                    pyautogui.hotkey('win', 'shift', 's')
                    time.sleep(1)


                # small every window
                elif index_up and middle_up and ring_up and pinky_up and thumb_up:
                    if lms[9].y > 0.7:
                        current_action = "SHOW DESKTOP"
                        pyautogui.hotkey('win', 'd')
                        time.sleep(1)


                # noise up down
                elif thumb_up and pinky_up and not index_up and not middle_up:
                    dist_vol = math.hypot(lms[4].x - lms[20].x, lms[4].y - lms[20].y)

                    if dist_vol > 0.15:
                        current_action = "VOLUME UP"
                        pyautogui.press('volumeup')
                    else:
                        current_action = "VOLUME DOWN"
                        pyautogui.press('volumedown')


                # finger move= mouse move
                elif index_up and not middle_up:
                    current_action = "MOVING CURSOR / MOUSE"

                    scr_x = int(lms[8].x * scr_breath)
                    scr_y = int(lms[8].y * scr_lenth)

                    # Smooth movement
                    curr_x = prev_x + (scr_x - prev_x) / smoothening
                    curr_y = prev_y + (scr_y - prev_y) / smoothening

                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y


                # SCROLL (INDEX + MIDDLE)
                elif index_up and middle_up:
                    if lms[8].y < 0.4:
                        current_action = "SCROLLING UP"
                        pyautogui.scroll(40)

                    elif lms[8].y > 0.6:
                        current_action = "SCROLING DOWN"
                        pyautogui.scroll(-40)


                # wring touch / DRAG (PINCH)
                dist_index_thumb = math.hypot(lms[8].x - lms[4].x,
                                             lms[8].y - lms[4].y)

                if dist_index_thumb < 0.04:

                    if pinch_go_time is None:
                        pinch_go_time = time.time()

                    elif time.time() - pinch_go_time > 0.5:
                        current_action = "DRAGGING"
                        if not kween:
                            pyautogui.mouseDown()
                            kween = True

                else:
                    if kween:
                        pyautogui.mouseUp()
                        kween = False
                        current_action = "DROP"

                    pinch_go_time = None


                # corekt touch 
                dist_middle_thumb = math.hypot(lms[12].x - lms[4].x,
                                              lms[12].y - lms[4].y)

                if dist_middle_thumb < 0.04:
                    current_action = "RIGHT CLICK!"

                    if not corekt_touching:
                        pyautogui.click()     
                        corekt_touching = True

                else:
                    corekt_touching = False


            # Draw 21 point on hnd
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hnd.HAND_CONNECTIONS)


    #top bar show what is doing
    cv2.rectangle(img, (0, 0), (w, 60), (0, 0, 0), -1)

    cv2.putText(img, f"STATUS: {current_action}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


    # heading for camera
    cv2.imshow("LIVE CAMERA", img)


    # close evt when i touch
    if cv2.waitKey(1) & 0xFF == ord('i'):
        break


#close evt
cap.release()
cv2.destroyAllWindows()
