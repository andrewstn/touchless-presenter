import cv2
import time
import pyautogui
import threading
from HandTrackingModule import HandDetector

pyautogui.PAUSE = 0

def main():
    cap = cv2.VideoCapture(0) # Change to 1 if needed
    detector = HandDetector(max_num_hands=1)
    
    cooldown_time = 2.0
    last_action_time = 0

    while True:
        success, img = cap.read()
        if not success:
            continue

        img = cv2.flip(img, 1)
        img = detector.find_hands(img, draw=True)
        fingers = detector.get_fingers_status()

        current_time = time.time()
        time_elapsed = current_time - last_action_time
        
        progress = min(time_elapsed / cooldown_time, 1.0)
        
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
                    # Spawn a background worker to press the key
                    threading.Thread(target=pyautogui.press, args=('right',)).start()
                    last_action_time = current_time
                    
            elif fingers == [1, 1, 0, 0]:
                cv2.putText(img, "Gesture: PREV", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 3)
                if progress == 1.0:
                    threading.Thread(target=pyautogui.press, args=('left',)).start()
                    last_action_time = current_time
                    
            elif fingers == [1, 1, 1, 1]:
                cv2.putText(img, "Gesture: EXIT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                if progress == 1.0:
                    threading.Thread(target=pyautogui.press, args=('esc',)).start()
                    last_action_time = current_time
            else:
                cv2.putText(img, "Waiting...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 3)

        cv2.imshow("Touchless Presenter", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()