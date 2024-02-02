import cv2
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import traceback

class captureClass():
    def __init__(self, cap_number):
        self.cap = cv2.VideoCapture(cap_number, cv2.CAP_DSHOW)

    def readFrame(self):
        ret, self.frame = self.cap.read()
        return ret

    def getFrame(self):
        return self.frame

    def capRelease(self):
        self.cap.release()

def threadCapture(cap_number1, cap_number2,cap_number3,cap_number4):
    final_frame_size = (1280, 960)  # 最終的な画像のサイズ
    single_frame_size = (640, 480)  # 個々のフレームのサイズ 
    cap_obj1 = captureClass(cap_number1)
    cap_obj2 = captureClass(cap_number2)
    cap_obj3 = captureClass(cap_number3)
    cap_obj4 = captureClass(cap_number4)


    while True:
        cap_obj1.readFrame()
        cap_obj2.readFrame()
        cap_obj3.readFrame()
        cap_obj4.readFrame()
        frame1 = cap_obj1.getFrame()
        frame2 = cap_obj2.getFrame()
        frame3 = cap_obj3.getFrame()
        frame4 = cap_obj4.getFrame()
        frame1 = cv2.resize(frame1, single_frame_size)
        frame2 = cv2.resize(frame2, single_frame_size)
        frame3 = cv2.resize(frame3, single_frame_size)
        frame4 = cv2.resize(frame4, single_frame_size)

        final_frame = np.zeros((final_frame_size[1], final_frame_size[0], 3), dtype=np.uint8)
        
        final_frame[0:480, 0:640] = frame1       # 左上
        final_frame[0:480, 640:1280] = frame2    # 右上
        final_frame[480:960, 0:640] = frame3     # 左下
        final_frame[480:960, 640:1280] = frame4  # 右下
        
        cv2.imshow("frame", final_frame)


        lastkey = cv2.waitKey(1)
        if lastkey == ord("q"):
            cap_obj1.release()
            cap_obj2.release()
            cap_obj3.release()
            cap_obj4.release()
            cv2.destroyAllWindows()
            break
        if lastkey == ord("c"):
            cv2.imwrite("frame.png", final_frame)


if __name__ == "__main__":

    cap_number1 = 0
    cap_number2 = 1
    cap_number3 = 2
    cap_number4 = 3
    
    executor = ThreadPoolExecutor(max_workers=4)
    camera_future = executor.submit(threadCapture, cap_number1, cap_number2,cap_number3,cap_number4)

    while True:
        if camera_future.running() == False:
            print("camera shutdown")
            executor.shutdown()
            break
        else:
            time.sleep(5)
            #print("5 seconds ...")

    print("program complete")
