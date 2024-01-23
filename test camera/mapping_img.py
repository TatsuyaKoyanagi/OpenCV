import cv2
import numpy as np
from matplotlib import pyplot as plt

path = 'igo.jpg'                                               # 画像のパス
i = cv2.imread(path, 1)                                        # 画像読み込み