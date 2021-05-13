import cv2

def capture():

    # 裁切區域的 x 與 y 座標（左上角）
    x = 600
    y = 270
    # 裁切區域的長度與寬度
    w = 750
    h = 750
    
    #cam = cv2.VideoCapture('http://192.168.0.123:8080/video?dummy=param.mjpg')
    cam = cv2.VideoCapture(0)
    
    # 設定影像的尺寸大小
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    
    cv2.namedWindow("CAPTURE")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        #cv2.imshow("capture", frame)

        img_name = "./testimage/capture.png"
        crop_frame = frame[y:y+h, x:x+w]
        cv2.imwrite(img_name, crop_frame)
        print("{} written!".format(img_name))
        break
        '''
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "capture.png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
        '''
    cam.release()
    cv2.destroyAllWindows()

    return 1
capture()
