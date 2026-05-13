import cv2
import time
import pyautogui

# Import our custom module!
from HandTrackingModule import HandDetector

def main():
    # 1. Setup Camera and variables
    cap = cv2.VideoCapture(0) # Change to 1 if needed for Mac continuity camera
    detector = HandDetector(max_num_hands=1)
    
    cooldown_time = 1.0
    last_action_time = 0

    # 2. Main Video Loop
    while True:
        success, img = cap.read()
        if not success:
            continue

        img = cv2.flip(img, 1)

        # Let our custom module handle the drawing!
        img = detector.find_hands(img, draw=True)
        
        # Ask our custom module which fingers are up
        fingers = detector.get_fingers_status()

        # 3. Presentation Logic
        if fingers: # If the array isn't empty (meaning a hand is on screen)
            current_time = time.time()
            
            if fingers == [1, 0, 0, 0]:
                cv2.putText(img, "Gesture: NEXT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press('right')
                    last_action_time = current_time
                    
            elif fingers == [1, 1, 0, 0]:
                cv2.putText(img, "Gesture: PREV", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 3)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press('left')
                    last_action_time = current_time
                    
            elif fingers == [1, 1, 1, 1]:
                cv2.putText(img, "Gesture: EXIT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                if current_time - last_action_time > cooldown_time:
                    pyautogui.press('esc')
                    last_action_time = current_time
                    
            else:
                cv2.putText(img, "Waiting...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 3)

        # 4. Display Window
        cv2.imshow("Touchless Presenter", img)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()

# This is standard Python practice. It ensures main() only runs if we execute THIS file.
if __name__ == "__main__":
    main()