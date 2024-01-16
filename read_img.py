# -*- coding: utf-8 -*-
import cv2	
path = "daihuku_sake.png"
img = cv2.imread(path)

cv2.imshow('imshow_test', img)
cv2.waitKey(0) 
cv2.destroyAllWindows()
