import cv2
def capture_camera(mirror=True, size=None):
 #カメラのキャプチャー
  cap = cv2.VideoCapture(0) #port番号
  while True:
   ret, frame = cap.read()
   if not ret:
    print("Failed to grab frame")
    break
   cv2.imshow('camera capture',frame)
   k=cv2.waitKey(1)
   if k==27:
     break
  cap.release()
  cv2.destroyAllWindows()
