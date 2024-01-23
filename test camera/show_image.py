import cv2
import numpy

if __name__ == "__main__":
    img = cv2.imread("./sample.png")
    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("window", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()