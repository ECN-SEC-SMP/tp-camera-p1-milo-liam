import cv2 as cv

ESC_KEY = 27
Q_KEY = 113
num_cam = 0

def main():
    windowName = "OpenCV Calibration"
    cv.namedWindow(windowName, cv.WINDOW_AUTOSIZE)

    index = 1
    while True:
        number = str(index)
        if len(number) == 1:
            number = "0" + number
        msg = "calib_gopro/GOPR84" +  number + ".JPG"
        print("image", msg)
        img_color = cv.imread(msg)

        img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)

        cv.imshow(windowName, img_color)

        key = cv.waitKey(500) & 0xFF  
        if key == ord('g'):
            cv.imshow(windowName, img_gray)
            cv.waitKey(500)
        elif key == ord('q') or key == 27:  
            break

        index += 1
        if index == 28:
            index = 1  

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
