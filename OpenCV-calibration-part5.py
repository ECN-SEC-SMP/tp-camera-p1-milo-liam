import cv2 as cv
import numpy as np
import glob

# Keycode definitions
ESC_KEY = 27
Q_KEY = 113

num_cam = 0

def main():
    # Critère de raffinement des coins
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Taille du damier (nombre de coins intérieurs)
    pattern_size = (9, 6)

    # Préparation des points 3D (fixes pour le damier)
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    objpoints = []  # points 3D 
    imgpoints = []  # points 2D 

    # Seuil pour la calibration 
    NUM_CALIB_IMAGES = 10

    # Choix de la caméra
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
    calibrated = False
    camera_matrix = None
    dist_coeffs = None

    print("Appuie sur 'c' pour enregistrer une image de calibration quand le damier est bien détecté.")
    print(f"Il faut {NUM_CALIB_IMAGES} images pour lancer la calibration.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Recherche du damier
        found, corners = cv.findChessboardCorners(
            gray,
            pattern_size,
            cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FILTER_QUADS
        )

        if found:
            # Raffiner les coins
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            # Dessiner les coins détectés
            cv.drawChessboardCorners(frame, pattern_size, corners2, found)

        # Gestion des touches
        key = cv.waitKey(1) & 0xFF
        if key == ord('g'):
            show_gray = not show_gray
        elif key == ord('c') and found:
            # On capture une image en appuyant sur c si le damier est trouvé 
            objpoints.append(objp.copy())
            imgpoints.append(corners2)
            print(f"Image de calibration enregistrée ({len(objpoints)}/{NUM_CALIB_IMAGES})")

            # On calibre si on a au moins 10 images 
            if len(objpoints) >= NUM_CALIB_IMAGES and not calibrated:
                print("==> Lancement de la calibration...")
                ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv.calibrateCamera(
                    objpoints, imgpoints, gray.shape[::-1], None, None
                )
                print("Calibration terminée.")
                print("\nMatrice intrinsèque (K) :\n", camera_matrix)
                print("\nCoefficients de distorsion :\n", dist_coeffs)
                calibrated = True
        
        elif key == ord('q'):
            break

        # Affichage selon le mode
        if show_gray:
            cv.imshow('frame', gray)
        else:
            cv.imshow('frame', frame)

        

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()