import cv2
from matplotlib import pyplot as plt

# 画像読み込み
img = cv2.imread("sample_25per.png")

# img[top : bottom, left : right]
# サンプル1の切り出し、保存
img1 = img[0 : 784, 0: 296]
cv2.imwrite("out_sample1.jpg", img1)

# ここからグラフ設定
cv2.imshow("window",img1)
cv2.waitKey(0)
cv2.destroyAllWindows()