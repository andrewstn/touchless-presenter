import cv2

# 1. Initialize the webcam. '0' is usually your default built-in laptop camera.
cap = cv2.VideoCapture(0)

# 2. Start the infinite loop to capture video frame-by-frame
while True:
    # Read the current frame from the webcam
    # 'success' is a boolean (True/False) if the frame was grabbed
    # 'img' is the actual image array
    success, img = cap.read()
    
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # 3. Flip the image horizontally so it acts like a mirror
    img = cv2.flip(img, 1)

    # 4. Show the image in a window named "Touchless Presenter"
    cv2.imshow("Touchless Presenter", img)

    # 5. Wait for 1 millisecond for a key press. If the user presses 'q', break the loop.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 6. Clean up: release the webcam and close the window
cap.release()
cv2.destroyAllWindows()