# -*- coding: utf-8 -*-

# 指定形式(BMP, TIFF, GIF, JPEG, PNG)の画像ファイルを開く場合
import cv2
 
if __name__ == '__main__':
	# 画像取得
	img = cv2.imread("MicrosoftTeams-image.png")
	# 画像表示
	cv2.imshow("Show Image", img)
	# キー入力待機
	cv2.waitKey(0)
	# 何かキーが押されたらウィンドウ破棄
	cv2.destroyAllWindows()
