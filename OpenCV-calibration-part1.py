
"""import numpy as np
import cv2 as cv
import os 

windowName = "OpenCV Calibration"
cv.namedWindow(windowName, cv.WINDOW_AUTOSIZE)

while True: 
    a = input("numéro de caméra ?")
    if int(a) == -1:
        print("extinction")
        os._exit(0)
    cap = cv.VideoCapture(int(a))
    if cap.isOpened():
        break
    else:
        print("un autre numéro stp")
        
while cap.isOpened():
    #print(cap.isOpened())
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow(windowName, gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()"""

# openCV import
import cv2 as cv

# Keycode definitions
ESC_KEY = 27
Q_KEY = 113

num_cam = 0

def main():
    # Define variables
    # A key that we use to store the user keyboard input
    key = None

while True:
    num_cam = int(input("Numéro de caméra (-1 pour quitter) : "))
    if num_cam == -1:
        exit()

    cap = cv.VideoCapture(num_cam)
    if cap.isOpened():
        break
    else:
        print("Caméra introuvable, réessayez.")
        cap.release()

show_gray = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    key = cv.waitKey(1) & 0xFF
    if key == ord('g'):
        show_gray = not show_gray

    if show_gray:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
    else:
        cv.imshow('frame', frame)

    if key == ord('q'):
        break

 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

# Starting the code
if __name__ == "__main__":
    main()
