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
            
            # 1. Get the height and width of the video frame
            h, w, c = img.shape

            # 2. Extract the Y-coordinates of the Index Finger Tip (8) and Knuckle (6)
            # MediaPipe outputs coordinates as percentages (0.0 to 1.0). 
            # We multiply by the frame height (h) to get the exact pixel location.
            index_tip_y = int(hand_landmarks.landmark[8].y * h)
            index_knuckle_y = int(hand_landmarks.landmark[6].y * h)

            # 3. The Logic: Is the tip higher up the screen than the knuckle?
            if index_tip_y < index_knuckle_y:
                # Draw green text on the screen
                cv2.putText(img, "Gesture: NEXT SLIDE", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            else:
                # Draw red text on the screen
                cv2.putText(img, "Waiting...", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Touchless Presenter", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()