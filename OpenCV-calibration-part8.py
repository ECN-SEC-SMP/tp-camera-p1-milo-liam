import cv2 as cv
import numpy as np

# Keycode definitions
ESC_KEY = 27
Q_KEY = 113

def main():
    folder = "calib_gopro/"
    show_gray = False
    show_undistorted = False
    index = 1

    # Critère de raffinement des coins
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Paramètres du damier
    nx = int(input("Nombre de coins intérieurs en largeur (ex: 9) : "))
    ny = int(input("Nombre de coins intérieurs en hauteur (ex: 6) : "))
    pattern_size = (nx, ny)

    # Préparation des points 3D (fixes pour le damier)
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    objpoints = []  # points 3D
    imgpoints = []  # points 2D

    calibrated = False
    camera_matrix = None
    dist_coeffs = None
    new_camera_mtx = None
    last_gray_shape = None

    print("==> Détection du damier sur les images du dossier calib_gopro/...")

    for idx in range(1, 28):  # de 1 à 27
        # Construction du nom de fichier
        filename = folder + "GOPR84"
        if idx < 10:
            filename += "0"
        filename += str(idx)
        filename += ".JPG"

        img = cv.imread(filename)
        if img is None:
            print(f"Impossible de lire {filename}, on saute.")
            continue

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        last_gray_shape = gray.shape[::-1]

        # Recherche du damier
        found, corners = cv.findChessboardCorners(
            gray,
            pattern_size,
            cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FILTER_QUADS
        )

        if found:
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp.copy())
            imgpoints.append(corners2)
            print(f"Damier trouvé sur {filename}")
        else:
            print(f"Damier NON trouvé sur {filename}")

    if len(objpoints) > 0:
        print("\n==> Lancement de la calibration...")
        ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv.calibrateCamera(
            objpoints, imgpoints, last_gray_shape, None, None
        )
        print("Calibration terminée.")
        print("\nMatrice intrinsèque (K) :\n", camera_matrix)
        print("\nCoefficients de distorsion :\n", dist_coeffs)

        # Calcul de la nouvelle matrice de caméra pour le redressement
        w, h = last_gray_shape
        new_camera_mtx, roi = cv.getOptimalNewCameraMatrix(
            camera_matrix, dist_coeffs, (w, h), 1, (w, h)
        )

        calibrated = True
        print("\nAppuie sur 'u' pour basculer entre image originale / redressée.")
    else:
        print("\nAucun damier détecté, calibration impossible.")
        print("Le diaporama affichera seulement les images originales.")

    print("Appuie sur 'g' pour couleur / gris.")
    print("Appuie sur 'q' pour quitter.\n")

    while True:
        # Construction du nom de fichier avec la méthode demandée
        filename = folder + "GOPR84"
        if index < 10:
            filename += "0"
        filename += str(index)
        filename += ".JPG"

        img = cv.imread(filename)

        if img is None:
            index = 1
            continue

        # Choix de l'image de base
        if calibrated and show_undistorted:
            output = cv.undistort(img, camera_matrix, dist_coeffs, None, new_camera_mtx)
        else:
            output = img

        # Option niveaux de gris
        if show_gray:
            output = cv.cvtColor(output, cv.COLOR_BGR2GRAY)

        cv.imshow('image', output)

        key = cv.waitKey(300) & 0xFF
        if key == ord('g'):
            show_gray = not show_gray
        elif key == ord('u') and calibrated:
            show_undistorted = not show_undistorted
        elif key == ord('q'):
            break

        index += 1
        if index > 27:
            index = 1

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()