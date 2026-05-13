import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0) # Or 1

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

            #Gesture Recognition Logic:
            h, w, c = img.shape
            
            # Create an empty list to store the status of our 4 fingers
            fingers = []

            # Finger IDs: Index(8,6), Middle(12,10), Ring(16,14), Pinky(20,18)
            tip_ids = [8, 12, 16, 20]
            knuckle_ids = [6, 10, 14, 18]

            # Loop through the 4 fingers and check if they are UP or DOWN
            for i in range(4):
                tip_y = hand_landmarks.landmark[tip_ids[i]].y
                knuckle_y = hand_landmarks.landmark[knuckle_ids[i]].y
                
                if tip_y < knuckle_y:
                    fingers.append(1) # Finger is UP
                else:
                    fingers.append(0) # Finger is DOWN
            
            # Pattern 1: ONLY the Index finger is up
            if fingers == [1, 0, 0, 0]:
                cv2.putText(img, "Gesture: NEXT SLIDE", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                            
            # Pattern 2: Index AND Middle fingers are up (Peace Sign)
            elif fingers == [1, 1, 0, 0]:
                cv2.putText(img, "Gesture: PREVIOUS SLIDE", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 3)
                            
            # Pattern 3: All fingers up (Open Palm)
            elif fingers == [1, 1, 1, 1]:
                cv2.putText(img, "Gesture: STOP", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                            
            # Default state when no specific gesture is matched
            else:
                cv2.putText(img, "Waiting...", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 3)

    cv2.imshow("Touchless Presenter", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()