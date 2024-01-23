import cv2
import numpy as np
from matplotlib import pyplot as plt

path = 'sample_25per.png'                                               # 画像のパス
i = cv2.imread(path, 1)                                        # 画像読み込み

# 変換前後の対応点を設定

p_original = np.float32([[0,0], [296,0], [296,784], [0,784]])
p_trans = np.float32([[0,0], [298,245], [296, 608], [0, 784]])

# 変換マトリクスと射影変換
M = cv2.getPerspectiveTransform(p_original, p_trans)
i_trans = cv2.warpPerspective(i, M, (296, 784))

# 画像保存
cv2.imwrite("changed.png", i_trans)

# ここからグラフ設定
fig = plt.figure()
ax1 = fig.add_subplot(111)

# 画像をプロット
show = cv2.cvtColor(i_trans, cv2.COLOR_BGR2RGB)
ax1.imshow(show)

fig.tight_layout()
plt.show()
plt.close()