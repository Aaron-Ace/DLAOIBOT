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
from capture import *
from latest_darknet_API import *
from analyzetxt import RecognizeItemPosition
from armcontrol import ArmControl
from XY2UV import *
from MotorCornorTranslateLoad import MotorAngle

#define
#Screw_Option=1,Nut_Option=2,Screw_Option+Nut_Option=3
#Size_Big_Option = 1, Size_Medium_Option=4, Size_Small_Option =7

# config
usbport = '/dev/ttyUSB0'

global queue
queue = queue.Queue()
global serial
serial = serial.Serial(usbport, 2000000, timeout=1)


def Yolo(detect):
    time.sleep(8)
    capture()
    latest_API(detect)
    position = RecognizeItemPosition()
    return position


def RoboticArm(detect, ObjectOption, SizeOption):

    position = Yolo(detect)
    for i in position:
        if(ObjectOption==1):
            if (SizeOption==1):
                if (i.category == "Screw" and i.size == 1):
                    queue.put(i)
            elif (SizeOption == 4):
                if (i.category == "Screw" and i.size == 2):
                    queue.put(i)
            elif (SizeOption == 5):
                if (i.category == "Screw" and (i.size == 1 or i.size == 2)):
                    queue.put(i)
            elif (SizeOption == 7):
                if (i.category == "Screw" and  i.size == 3):
                    queue.put(i)
            elif (SizeOption == 8):
                if (i.category == "Screw" and (i.size == 1 or i.size == 3)):
                    queue.put(i)
            elif (SizeOption == 11):
                if (i.category == "Screw" and (i.size == 2 or i.size == 3)):
                    queue.put(i)
            elif (SizeOption == 12):
                if (i.category == "Screw"):
                    queue.put(i)
            else:
                print("Error Sizes Option")
        elif(ObjectOption==2):
            if (SizeOption==1):
                if (i.category == "Nut" and i.size == 1):
                    queue.put(i)
            elif (SizeOption == 4):
                if (i.category == "Nut" and i.size == 2):
                    queue.put(i)
            elif (SizeOption == 5):
                if (i.category == "Nut" and (i.size == 1 or i.size == 2)):
                    queue.put(i)
            elif (SizeOption == 7):
                if (i.category == "Nut" and  i.size == 3):
                    queue.put(i)
            elif (SizeOption == 8):
                if (i.category == "Nut" and (i.size == 1 or i.size == 3)):
                    queue.put(i)
            elif (SizeOption == 11):
                if (i.category == "Nut" and (i.size == 2 or i.size == 3)):
                    queue.put(i)
            elif (SizeOption == 12):
                if (i.category == "Nut"):
                    queue.put(i)
            else:
                print("Error Sizes Option")
        elif(ObjectOption==3):
            if (SizeOption==1):
                if (i.size == 1):
                    queue.put(i)
            elif (SizeOption == 4):
                if (i.size == 2):
                    queue.put(i)
            elif (SizeOption == 5):
                if ((i.size == 1 or i.size == 2)):
                    queue.put(i)
            elif (SizeOption == 7):
                if (i.size == 3):
                    queue.put(i)
            elif (SizeOption == 8):
                if ((i.size == 1 or i.size == 3)):
                    queue.put(i)
            elif (SizeOption == 11):
                if ((i.size == 2 or i.size == 3)):
                    queue.put(i)
            elif (SizeOption == 12):
                    queue.put(i)
            else:
                print("Error Sizes Option")
        else:
            print("Error Object Option")
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
        queue.queue.clear()
        position = Yolo(detect)
        for i in position:
            if (ObjectOption == 1):
                if (SizeOption == 1):
                    if (i.category == "Screw" and i.size == 1):
                        queue.put(i)
                elif (SizeOption == 4):
                    if (i.category == "Screw" and i.size == 2):
                        queue.put(i)
                elif (SizeOption == 5):
                    if (i.category == "Screw" and (i.size == 1 or i.size == 2)):
                        queue.put(i)
                elif (SizeOption == 7):
                    if (i.category == "Screw" and i.size == 3):
                        queue.put(i)
                elif (SizeOption == 8):
                    if (i.category == "Screw" and (i.size == 1 or i.size == 3)):
                        queue.put(i)
                elif (SizeOption == 11):
                    if (i.category == "Screw" and (i.size == 2 or i.size == 3)):
                        queue.put(i)
                elif (SizeOption == 12):
                    if (i.category == "Screw"):
                        queue.put(i)
                else:
                    print("Error Sizes Option")
            elif (ObjectOption == 2):
                if (SizeOption == 1):
                    if (i.category == "Nut" and i.size == 1):
                        queue.put(i)
                elif (SizeOption == 4):
                    if (i.category == "Nut" and i.size == 2):
                        queue.put(i)
                elif (SizeOption == 5):
                    if (i.category == "Nut" and (i.size == 1 or i.size == 2)):
                        queue.put(i)
                elif (SizeOption == 7):
                    if (i.category == "Nut" and i.size == 3):
                        queue.put(i)
                elif (SizeOption == 8):
                    if (i.category == "Nut" and (i.size == 1 or i.size == 3)):
                        queue.put(i)
                elif (SizeOption == 11):
                    if (i.category == "Nut" and (i.size == 2 or i.size == 3)):
                        queue.put(i)
                elif (SizeOption == 12):
                    if (i.category == "Nut"):
                        queue.put(i)
                else:
                    print("Error Sizes Option")
            elif (ObjectOption == 3):
                if (SizeOption == 1):
                    if (i.size == 1):
                        queue.put(i)
                elif (SizeOption == 4):
                    if (i.size == 2):
                        queue.put(i)
                elif (SizeOption == 5):
                    if ((i.size == 1 or i.size == 2)):
                        queue.put(i)
                elif (SizeOption == 7):
                    if (i.size == 3):
                        queue.put(i)
                elif (SizeOption == 8):
                    if ((i.size == 1 or i.size == 3)):
                        queue.put(i)
                elif (SizeOption == 11):
                    if ((i.size == 2 or i.size == 3)):
                        queue.put(i)
                elif (SizeOption == 12):
                    queue.put(i)
                else:
                    print("Error Sizes Option")
            else:
                print("Error Object Option")

def mainfunc():
    detect = Detect(metaPath=r'./cfg/obj.data',
                    configPath=r'./cfg/yolo-obj.cfg',
                    weightPath=r'./backup/yolo-obj_last.weights',
                    gpu_id=0)
    file = open('OptionCheckList.ini', 'r')
    log =[]
    for line in file:
        if(line.find('Screw_Option:') != -1):
            Screw_Option = int(line[line.find('Screw_Option:')+13:line.find('Screw_Option:')+14])
            if Screw_Option != -1:
                log.append(Screw_Option)
        if (line.find('Nut_Option:') != -1):
            Nut_Option   = int(line[line.find('Nut_Option:') + 11:line.find('Nut_Option:') + 12])
            if Nut_Option != -1:
                log.append(Nut_Option)
        if (line.find('Size_Big_Option:') != -1):
            Size_Big_Option    = int(line[line.find('Size_Big_Option:') + 16:line.find('Size_Big_Option:') + 17])
            if Size_Big_Option != -1:
                log.append(Size_Big_Option)
        if (line.find('Size_Medium_Option:') != -1):
            Size_Medium_Option = int(line[line.find('Size_Medium_Option:') + 19:line.find('Size_Medium_Option:') + 20])
            if Size_Medium_Option != -1:
                log.append(Size_Medium_Option)
        if (line.find('Size_Small_Option:') != -1):
            Size_Small_Option  = int(line[line.find('Size_Small_Option:') + 18:line.find('Size_Small_Option:') + 19])
            if Size_Small_Option != -1:
                log.append(Size_Small_Option)
    file.close()

    ObjectOption = log[0]*1+log[1]*2
    SizeOption   = log[2]*1+log[3]*4+log[4]*7

    RoboticArm(detect, ObjectOption, SizeOption)

if __name__ == '__main__':
    mainfunc()




