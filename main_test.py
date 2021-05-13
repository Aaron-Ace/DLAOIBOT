import time
from threading import Thread
from capture import *
from latest_darknet_API import *
from analyzetxt import RecognizeItemPosition

#config
timesleep = 3

def Yolo():
    detect = Detect(metaPath=r'./cfg/obj.data',
                    configPath=r'./cfg/yolo-obj.cfg',
                    weightPath=r'./backup/yolo-obj_last.weights',
                    gpu_id=0)
    while (True):
        capture()
        latest_API(detect)
        position = RecognizeItemPosition()
        time.sleep(timesleep)

if __name__ == '__main__':
    Yolo()



