#********************
#   NDHU    CSIE    *
#  Author:Aaronace  *
#    2020-2021      *
#  GraduateProject  *
#   Professor:CCC   *
#********************

import serial
import time
def ArmControl(serial,Angle,size,object):
    if(object=="Screw"):
        obj = 1
    else:
        obj = 2
    try:
        global data
        data = str(Angle[0]).zfill(3)+str(Angle[1]).zfill(3)+str(Angle[2]).zfill(3)+str(Angle[3]).zfill(3)+\
               str(Angle[4]).zfill(3)+str(Angle[5]).zfill(3)+str(size)+str(obj)
        #print(data)
        time.sleep(5)
        serial.write(str(data).encode())
        return 1
    except:
        print("Control Failed")
        return 0


if __name__ == '__main__':
    ArmControl(serial.Serial('/dev/ttyUSB0', 2000000, timeout=5),[55,95,95,70,158,115],2)
#0650940910701580901
