# ********************
#   NDHU    CSIE    *
#  Author:Aaronace  *
#    2020-2021      *
#  GraduateProject  *
#   Professor:CCC   *
# ********************

import time
import queue
import serial
from threading import Thread
from capture import *
from latest_darknet_API import *
from analyzetxt import RecognizeItemPosition
from armcontrol import ArmControl
from XY2UV import *
from MotorCornorTranslateLoad import MotorAngle

# config
timesleep = 5
usbport = '/dev/ttyUSB0'

global queue
queue = queue.Queue()
global serial
serial = serial.Serial(usbport, 2000000, timeout=1)


def Yolo():
    capture()
    latest_API(detect)
    position = RecognizeItemPosition()
    return position


def RoboticArm():

    position = Yolo()
    for i in position:
        queue.put(i)
    while (queue.empty() == False):
        item = queue.get()
        # print(item.y)
        UV = xy2uv(item.x, item.y)
        Angle = MotorAngle(UV[0], UV[1])
        Angle[1] = Angle[1]-4
        Angle[4] = Angle[4]-2
        Angle[5] = Angle[5]+25
        ArmControl(serial,Angle, item.size, item.category)
        #ArmControl(serial, [65, 94, 91, 70, 158, 90], 1)
        time.sleep(10)
        queue.queue.clear()
        position = Yolo()
        for i in position:
            queue.put(i)
            #print(len(queue.queue))



if __name__ == '__main__':
    detect = Detect(metaPath=r'./cfg/obj.data',
                    configPath=r'./cfg/yolo-obj.cfg',
                    weightPath=r'./backup/yolo-obj_last.weights',
                    gpu_id=0)
    RoboticArm()




