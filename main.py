import cv2
import mediapipe as mp
import pyautogui
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0) # Or 1

# Cooldown mechanism to prevent multiple key presses from a single gesture
cooldown_time = 1.0  # Wait 1 second between gestures
last_action_time = 0 # Keeps track of when we last pressed a key


while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, c = img.shape
            fingers = []
            tip_ids = [8, 12, 16, 20]
            knuckle_ids = [6, 10, 14, 18]

            for i in range(4):
                tip_y = hand_landmarks.landmark[tip_ids[i]].y
                knuckle_y = hand_landmarks.landmark[knuckle_ids[i]].y
                
                if tip_y < knuckle_y:
                    fingers.append(1) 
                else:
                    fingers.append(0) 

            # Get the current time to manage cooldown
            current_time = time.time()
            
            # Pattern 1: NEXT SLIDE (Only Index Up)
            if fingers == [1, 0, 0, 0]:
                cv2.putText(img, "Gesture: NEXT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                
                # Check if enough time has passed since the last action
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press('right') # Press the right arrow key!
                    last_action_time = current_time
                            
            # Pattern 2: PREVIOUS SLIDE (Index & Middle Up)
            elif fingers == [1, 1, 0, 0]:
                cv2.putText(img, "Gesture: PREV", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 3)
                
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press('left') # Press the left arrow key!
                    last_action_time = current_time
                            
            # Pattern 3: STOP / EXIT (All fingers up)
            elif fingers == [1, 1, 1, 1]:
                cv2.putText(img, "Gesture: EXIT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press('esc') # Press the Escape key!
                    last_action_time = current_time
                            
            else:
                cv2.putText(img, "Waiting...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 3)

    cv2.imshow("Touchless Presenter", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()