import cv2
import time
import pyautogui
import threading
import sys
from HandTrackingModule import HandDetector

pyautogui.PAUSE = 0

# Application Configuration
CONFIG = {
    "CAMERA_INDEX": 0,       # Change to 1 for Mac Continuity Camera
    "COOLDOWN_TIME": 2.0,    # Seconds to wait between gestures
    "KEYS": {
        "NEXT": "right",
        "PREV": "left",
        "EXIT": "esc"
    }
}


def main():
    print("Initializing Touchless Presenter...")
    
    # Start camera using the config
    cap = cv2.VideoCapture(CONFIG["CAMERA_INDEX"])
    
    # Camera verification
    if not cap.isOpened():
        print(f"\n[ERROR] Could not access camera at index {CONFIG['CAMERA_INDEX']}.")
        print("-> Please check your Mac Privacy & Security settings.")
        print("-> Or try changing CAMERA_INDEX to 1 in the CONFIG dictionary.")
        cap.release()
        cv2.destroyAllWindows()
        sys.exit() # Cleanly stop the script

    detector = HandDetector(max_num_hands=1)
    last_action_time = 0

    print("[SUCCESS] System Ready. Press 'q' in the video window to quit.")

    try:
        while True:
            success, img = cap.read()
            if not success:
                print("[WARNING] Ignored empty camera frame.")
                time.sleep(0.1) # Pause briefly to prevent freezing
                continue

            img = cv2.flip(img, 1)
            img = detector.find_hands(img, draw=True)
            fingers = detector.get_fingers_status()

            current_time = time.time()
            time_elapsed = current_time - last_action_time
            progress = min(time_elapsed / CONFIG["COOLDOWN_TIME"], 1.0)
            
            bar_x, bar_y = 50, 100
            bar_width, bar_height = 400, 30
            fill_width = int(bar_width * progress)
            
            if progress == 1.0:
                bar_color = (0, 255, 0) 
                cv2.putText(img, "STATUS: READY", (50, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, bar_color, 2)
            else:
                bar_color = (0, 165, 255) 
                cv2.putText(img, "STATUS: COOLDOWN", (50, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, bar_color, 2)

            cv2.rectangle(img, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 3)
            cv2.rectangle(img, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), bar_color, cv2.FILLED)

            if fingers: 
                if fingers == [1, 0, 0, 0]:
                    cv2.putText(img, "Gesture: NEXT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    if progress == 1.0: 
                        # Using the CONFIG dictionary instead of hardcoded strings
                        threading.Thread(target=pyautogui.press, args=(CONFIG["KEYS"]["NEXT"],)).start()
                        last_action_time = current_time
                        
                elif fingers == [1, 1, 0, 0]:
                    cv2.putText(img, "Gesture: PREV", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 3)
                    if progress == 1.0:
                        threading.Thread(target=pyautogui.press, args=(CONFIG["KEYS"]["PREV"],)).start()
                        last_action_time = current_time
                        
                elif fingers == [1, 1, 1, 1]:
                    cv2.putText(img, "Gesture: EXIT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    if progress == 1.0:
                        threading.Thread(target=pyautogui.press, args=(CONFIG["KEYS"]["EXIT"],)).start()
                        last_action_time = current_time
                else:
                    cv2.putText(img, "Waiting...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 3)

            cv2.imshow("Touchless Presenter", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        # If any weird error happens during runtime, catch it and print it nicely
        print(f"\n[CRITICAL ERROR] The application crashed: {e}")
        
    finally:
        # Release camera and close windows cleanly, even if an error occurs
        print("\n[INFO] Shutting down cleanly. Releasing camera...")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()