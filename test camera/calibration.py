import cv2
import numpy as np

# カメラマトリックスと歪み係数
cameraMatrix = np.array([[503.68477278, 0, 313.67563674],
                         [0, 503.37989194, 243.25575476],
                         [0, 0, 1]])
distCoeffs = np.array([2.08346324e-01, -4.68650266e-01, 4.51079181e-04, -1.93373893e-03, 2.37592401e-01])

# 補正したい画像を読み込む
image = cv2.imread('out_sample1.jpg')

# 歪み補正を適用
undistorted_image = cv2.undistort(image, cameraMatrix, distCoeffs, None)

# 結果を表示
cv2.imshow('Undistorted Image', undistorted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
