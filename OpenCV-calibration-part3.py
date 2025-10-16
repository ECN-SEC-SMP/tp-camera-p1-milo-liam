import cv2 as cv
import numpy as np


CRIT = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
window = "calibration"
cv.namedWindow(window, cv.WINDOW_AUTOSIZE)


def main():
    #ouverture cam 
    """while True:
        num_cam = int(input("Numéro de caméra (-1 pour quitter) : "))
        if num_cam == -1:
            exit()
        cap = cv.VideoCapture(num_cam)
        if not cap.isOpened():
            print("Caméra introuvable, réessayez.")
            cap.release()
        else: 
            print('super la cam')
            break"""
    cap = cv.VideoCapture(0)
    while True:
        ok, frame = cap.read()
        if ok : 
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            echiquier, corners = cv.findChessboardCorners(gray, (9,6))

            img_show = frame.copy()

            if echiquier: #on a trouvé un truc !!
                corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), CRIT) #on précise
                cv.drawChessboardCorners(img_show, (9,6), corners2, True)
                #print("echiquier trouvé")
            #else:
                #print("rien trouvé")

            cv.imshow(window, img_show)

            key = cv.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):
                break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
