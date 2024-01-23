import cv2
import numpy

if __name__ == "__main__":
    Img1 = cv2.imread("./cat1.jpg")
    Img2 = cv2.imread("./cat2.jpg")
    Img3 = cv2.imread("./cat2.jpg")
    mergeImg = numpy.hstack((Img1, Img2,Img3))
    cv2.imshow("sample", mergeImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()