import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
# Set up the hand tracking model:
# - max_num_hands=1: We only need to track one hand to control a presentation.
# - min_detection_confidence=0.7: strictness to prevent false positives in the background.
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)
# A handy utility to draw the lines and dots for us
mp_draw = mp.solutions.drawing_utils

# Remember to keep this as 0 or 1, whichever worked for you!
cap = cv2.VideoCapture(0) 

while True:
    success, img = cap.read()
    if not success:
        continue

    # Flip the image horizontally so it acts like a mirror
    img = cv2.flip(img, 1)

    # OpenCV uses BGR colors by default, but MediaPipe expects RGB.
    # We MUST convert the color space before feeding it to the AI.
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Pass the RGB image to the model to find hands
    results = hands.process(img_rgb)

    # If the AI found a hand in this specific frame...
    if results.multi_hand_landmarks:
        # Loop through each hand found (even though we capped it at 1)
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw the 21 dots and the connecting lines on our original 'img'
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the final image with the drawings on it
    cv2.imshow("Touchless Presenter", img)

    # Wait for 1 millisecond for a key press. Press 'q' to break the loop.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()