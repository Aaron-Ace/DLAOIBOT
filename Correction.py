import cv2
import numpy as np
from capture import capture

def Calc(w, h, k ,m, img):
    A = np.zeros([1, 2], dtype=int)
    for i in range(w, h):
        for j in range(k, m):
            if (img[j, i] == 0):
                B = np.array([[j, i]], dtype=int)
                A = np.append(A, B, axis=0)

    A = np.delete(A, 0, axis=0)
    sum_j = 0
    sum_i = 0
    for i in range(0, len(A)):
        sum_j += A[i][0]
        sum_i += A[i][1]
    mean_j = int(sum_j / len(A))
    mean_i = int(sum_i / len(A))
    temp = np.array([[mean_i, mean_j]])
    return  temp


def Correction():
    capture()
    # 讀取影像作成二值化
    img = cv2.imread('./testimage/capture.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, out = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)

    # 形態處理
    for i in range(0, 30):
        for j in range(0, 750):
            out[j, i] = 255

    # 黑點決策
    corner = np.zeros((1, 2), dtype=int)

    # 左上
    corner = np.append(corner, Calc(0,375,0,375, out), axis=0)
    # 右上
    corner = np.append(corner, Calc(375,750,0,375, out), axis=0)
    # 左下
    corner = np.append(corner, Calc(0, 375, 375, 750 ,out), axis=0)
    # 右下
    corner = np.append(corner, Calc(375, 750, 375, 750, out), axis=0)

    # 黑點輸出
    corner = np.delete(corner, 0, axis=0)

    file = open('pixel_position.ini','w+')
    file.write('left_top_x:'+str(corner[0][0]).zfill(3)+' left_top_y:'+str(corner[0][1]).zfill(3)+ \
                ' right_top_x:'+str(corner[1][0]).zfill(3)+' right_top_y:'+str(corner[1][1]).zfill(3)+ \
                ' left_bottom_x:'+str(corner[2][0]).zfill(3)+' left_bottom_y:'+str(corner[2][1]).zfill(3)+\
                ' right_bottom_x:'+str(corner[3][0]).zfill(3)+' right_bottom_y:'+str(corner[3][1]).zfill(3))
    file.close()
    print(corner)

if __name__ == '__main__':
    Correction()
