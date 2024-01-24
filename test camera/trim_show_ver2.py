# インポートするパッケージ
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import configparser
import os
import sys

# 日本語パス対応のためのimread関数作成
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

# 日本語パス対応のためのimwrite関数作成
def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

# マウス位置のリスト作成処理
class PointList():
    def __init__(self, npoints):
        self.npoints = npoints
        self.ptlist = np.empty((npoints, 2), dtype=int)
        self.pos = 0

    # マウス位置追加保存処理
    def add(self, x, y):
        if self.pos < self.npoints:
            self.ptlist[self.pos, :] = [x, y]
            self.pos += 1
            return True
        return False

# 拡大縮小にて処理方法を変更するためにチェックを行う処理
def SizeCheck(thresh,size,img):
    orgHeight, orgWidth = img.shape[:2]
    if thresh > orgWidth:
        # 拡大処理　INTER_CUBIC
        return cv2.resize(img, size, interpolation = cv2.INTER_CUBIC) 
    else:
        # 縮小処理　IINTER_AREA
        return cv2.resize(img, size, interpolation = cv2.INTER_AREA)

# マウス・クリック位置表示処理
def onMouse(event, x, y, flag, params):
    wname, img, ptlist = params
    if event == cv2.EVENT_MOUSEMOVE:  # マウスが移動したときにx線とy線を更新する
        img2 = np.copy(img)
        h, w = img2.shape[0], img2.shape[1]
        cv2.line(img2, (x, 0), (x, h - 1), (255, 0, 0))
        cv2.line(img2, (0, y), (w - 1, y), (255, 0, 0))
        cv2.imshow(wname, img2)

    if event == cv2.EVENT_LBUTTONDOWN:  # レフトボタンをクリックしたとき、ptlist配列にx,y座標を格納する
        if ptlist.add(x, y):
            print('[%d] ( %d, %d )' % (ptlist.pos - 1, x, y))
            cv2.circle(img, (x, y), 3, (0, 0, 255), 3)
            cv2.imshow(wname, img)
        else:
            print('All points have selected.  Press ESC-key.')
        if(ptlist.pos == ptlist.npoints):
            cv2.line(img, (ptlist.ptlist[0][0], ptlist.ptlist[0][1]),
                     (ptlist.ptlist[1][0], ptlist.ptlist[1][1]), (0, 255, 0), 3)
            cv2.line(img, (ptlist.ptlist[1][0], ptlist.ptlist[1][1]),
                     (ptlist.ptlist[2][0], ptlist.ptlist[2][1]), (0, 255, 0), 3)
            cv2.line(img, (ptlist.ptlist[2][0], ptlist.ptlist[2][1]),
                     (ptlist.ptlist[3][0], ptlist.ptlist[3][1]), (0, 255, 0), 3)
            cv2.line(img, (ptlist.ptlist[3][0], ptlist.ptlist[3][1]),
                     (ptlist.ptlist[0][0], ptlist.ptlist[0][1]), (0, 255, 0), 3)
            cv2.imshow(wname, img)

class Main():
    def __init__(self,file_path,file_Name):
        # 画像読み込み処理と射影範囲選択処理用画像作成
        self.img = imread(file_path,cv2.IMREAD_COLOR)
        self.orgHeight, self.orgWidth = self.img.shape[:2]
        # 幅の小さい方に合わせて画像作成を行う
        self.sizeH = (int(self.orgWidth*700/self.orgHeight),700)
        self.sizeW = (1000,int(self.orgHeight*1000/self.orgWidth))
        if self.sizeH[0] > self.sizeW[0]:
            self.ratio = 1000/self.orgWidth
            # 拡大縮小用の関数
            self.ImgShow = SizeCheck(self.sizeW[0],self.sizeW,self.img)
        else:
            self.ratio = 700/self.orgHeight
            # 拡大縮小用の関数
            self.ImgShow = SizeCheck(self.sizeH[0],self.sizeH,self.img)
        # 画面からのマウスイベント取得用設定
        self.wname = "MouseEvent"
        cv2.namedWindow(self.wname)
        self.npoints = 4
        self.ptlist = PointList(self.npoints)
        cv2.setMouseCallback(self.wname, onMouse, [self.wname, self.ImgShow, self.ptlist])
        cv2.imshow(self.wname, self.ImgShow)
        cv2.waitKey()
        cv2.destroyAllWindows()
        
        # 変換前後の対応点を設定 p1-p4はそれぞれ対応しているので順番通りに選択が必要
        self.p_original = np.float32([[int(x/self.ratio) for x in self.ptlist.ptlist[0]], \
            [int(x/self.ratio) for x in self.ptlist.ptlist[1]],\
            [int(x/self.ratio) for x in self.ptlist.ptlist[2]],\
            [int(x/self.ratio) for x in self.ptlist.ptlist[3]]])
        self.diff_width1 = np.abs(int(self.ptlist.ptlist[0][0]/self.ratio) - int(self.ptlist.ptlist[1][0]/self.ratio))
        self.diff_width2 = np.abs(int(self.ptlist.ptlist[2][0]/self.ratio) - int(self.ptlist.ptlist[3][0]/self.ratio))
        self.diff_height1 = np.abs(int(self.ptlist.ptlist[0][1]/self.ratio) - int(self.ptlist.ptlist[3][1]/self.ratio))
        self.diff_height2 = np.abs(int(self.ptlist.ptlist[1][1]/self.ratio) - int(self.ptlist.ptlist[2][1]/self.ratio))
        # 幅と高さの小さい方に合わせる。
        if self.diff_width1 < self.diff_width2:
            self.width = self.diff_width1
        else:
            self.width = self.diff_width2
        if self.diff_height1 < self.diff_height2:
            self.height = self.diff_height1
        else:
            self.height = self.diff_height2
        self.p_trans = np.float32([[0,0], [self.width,0], [self.width,self.height], [0,self.height]])
        
        # 変換マトリクスと射影変換
        self.M = cv2.getPerspectiveTransform(self.p_original, self.p_trans)
        self.img_trans = cv2.warpPerspective(self.img,self.M, (self.width,self.height))
        self.ImgCut = self.img_trans

        self.ImgCutHeight, self.ImgCutWidth = self.ImgCut.shape[:2]
        # 射影した画像のサイズ調整
        self.size = (780,int(self.ImgCutHeight*780/self.ImgCutWidth))

        self.ImgShow = SizeCheck(780,self.size,self.ImgCut)
        # ファイルを元の名称+"-fix"+拡張子にて保存
        basename = os.path.basename(file_path)
        dirname = os.path.dirname(file_path)
        root, ext = os.path.splitext(file_path)
        imwrite(dirname +'/'+ file_Name +'-fix' + ext, self.ImgShow)

if __name__ == "__main__":
    # 引数からのファイルフルパス配列取得
    args = sys.argv
    for i,file_path in enumerate(args):
        # 拡張子取得と拡張子チェック処理
        root, ext = os.path.splitext(file_path)
        if ext.lower() == '.png' or ext.lower() == '.jpg' or ext.lower() == '.jpeg' or ext.lower() == '.webp':
            # 現在のファイル名取得
            file_Name = os.path.splitext(os.path.basename(file_path))[0]
            main = Main(file_path,file_Name)