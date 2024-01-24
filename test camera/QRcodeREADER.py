import cv2
import webbrowser
from tkinter import messagebox

delay = 1
window_name = 'OpenCV QR Code'

qcd = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)

flag = True

while flag == True:
    ret, frame = cap.read()
    if ret:
        ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_info, points):
                if s:
                    print(s)
                    color = (0, 255, 0)
                    # QRコードから得られたテキストがURLの場合、ブラウザで開く
                    if s.startswith('http://') or s.startswith('https://'):
                        response = messagebox.askyesno("URLを開きますか？", f"このURLを開きますか？\n{s}")
                        if response:
                            frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
                            webbrowser.open(s)   
                            flag = False                       
                else:
                    color = (0, 0, 255)
                frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
        cv2.imshow(window_name, frame)

    if cv2.waitKey(delay) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
