import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        """Initializes the MediaPipe Hands model."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Store the IDs for the tips and knuckles of the 4 main fingers
        self.tip_ids = [8, 12, 16, 20]
        self.knuckle_ids = [6, 10, 14, 18]
        self.results = None

    def find_hands(self, img, draw=True):
        """Processes the image, finds hands, and optionally draws the skeleton."""
        # MediaPipe needs RGB, but OpenCV provides BGR
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        # Draw the landmarks if a hand is found and draw is True
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_fingers_status(self):
        """Returns a list of 1s (UP) and 0s (DOWN) for the 4 main fingers."""
        fingers = []
        
        # If we successfully found a hand in the current frame
        if self.results and self.results.multi_hand_landmarks:
            # Grab the landmarks for the first hand detected
            hand_landmarks = self.results.multi_hand_landmarks[0]
            
            # Loop through our 4 fingers to check if they are up or down
            for i in range(4):
                tip_y = hand_landmarks.landmark[self.tip_ids[i]].y
                knuckle_y = hand_landmarks.landmark[self.knuckle_ids[i]].y
                
                if tip_y < knuckle_y:
                    fingers.append(1) # Finger is UP
                else:
                    fingers.append(0) # Finger is DOWN
                    
        return fingers