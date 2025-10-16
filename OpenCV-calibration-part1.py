"""# openCV import
import cv2 as cv

# Keycode definitions
ESC_KEY = 27
Q_KEY = 113

def main():
    # Define variables
    # A key that we use to store the user keyboard input
    key = None
# Starting the code
if __name__ == "__main__":
    main()
"""

import numpy as np
import cv2 as cv
import os 

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
    print(cap.isOpened())
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

