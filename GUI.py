from tkinter import *
import cv2
import serial
import sys
from Correction import *
from main import mainfunc

def writefile():
    id  =['Screw_Option:','Nut_Option:','Size_Big_Option:','Size_Medium_Option:','Size_Small_Option:']
    file = open("OptionCheckList.ini", "w")
    file.write(id[0]+str(Screw.get())+"\n")
    file.write(id[1]+str(Nut.get())+"\n")
    file.write(id[2]+str(Big.get())+"\n")
    file.write(id[3]+str(Mid.get())+"\n")
    file.write(id[4]+str(Small.get())+"\n")
    file.close()

def ScrewIsChecked():
    writefile()

def NutIsChecked():
    writefile()

def BigIsChecked():
    writefile()

def MidIsChecked():
    writefile()

def SmallIsChecked():
    writefile()

def CameraCheck():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        CameraStatus = Button(ws, text='Failed', padx=10, pady=5, state=DISABLED, bg="red", fg="white").place(x=290, y=0)

    else:
        CameraStatus = Button(ws, text='Sucessful', padx=10, pady=5, state=DISABLED, bg="green", fg="white").place(x=290, y=0)

def SerialCheck():
    usbport = '/dev/ttyUSB0'
    serials = serial.Serial(usbport, 2000000, timeout=1)
    if(serials):
        SerialStatus = Button(ws, text='Sucessful', padx=10, pady=5, state=DISABLED, bg="green", fg="white").place(x=290, y=50)
    else:
        SerialStatus = Button(ws, text='Failed', padx=10, pady=5, state=DISABLED, bg="red", fg="white").place(x=290, y=50)


def Correct():
    Correction()
def ForceStop():
    sys.exit()
def Execute():
    mainfunc()
    pass
if __name__ == '__main__':
    ws = Tk()
    ws.title('PythonGuides')
    ws.geometry('380x300')

    Cameratext = Button(ws, text='Camera Connect', padx=30, pady=5, state=DISABLED)
    Cameratext.place(x=110,y=0)
    CameraStatus = Button(ws, text='Status', padx=10, pady=5, state=DISABLED).place(x=290, y=0)
    CameraCheckbtn = Button(ws, text='Check', padx=20, pady=5, command=CameraCheck).place(x=10,y=0)

    Serialtext = Button(ws, text='Serial Port', padx=50, pady=5, state=DISABLED).place(x=110,y=50)
    SerialStatus = Button(ws, text='Status', padx=10, pady=5, state=DISABLED).place(x=290, y=50)
    SerialCheckbtn = Button(ws, text='Check', padx=20, pady=5, command=SerialCheck).place(x=10,y=50)

    file = open('OptionCheckList.ini', 'r')

    Screw = IntVar()
    Nut   = IntVar()
    Big   = IntVar()
    Mid   = IntVar()
    Small = IntVar()
    for line in file:
        if (line.find('Screw_Option:') == 0):
            Checkbutton(ws, text="Screw" , variable=Screw, onvalue=1, offvalue=0, command=ScrewIsChecked).place(x=5,y=100)
            Screw.set(int(line[line.find('Screw_Option:') + 13:line.find('Screw_Option:') + 14]))
        if (line.find('Nut_Option:') == 0):
            Checkbutton(ws, text=" Nut " , variable=Nut, onvalue=1, offvalue=0, command=NutIsChecked).place(x=105,y=100)
            Nut.set(int(line[line.find('Nut_Option:') + 11:line.find('Nut_Option:') + 12]))
        if (line.find('Size_Big_Option:') == 0):
            Checkbutton(ws, text=" Big " , variable=Big, onvalue=1, offvalue=0, command=BigIsChecked).place(x=5,y=150)
            Big.set(int(line[line.find('Size_Big_Option:') + 16:line.find('Size_Big_Option:') + 17]))
        if (line.find('Size_Medium_Option:') == 0):
            Checkbutton(ws, text="Medium", variable=Mid, onvalue=1, offvalue=0, command=MidIsChecked).place(x=105,y=150)
            Mid.set(int(line[line.find('Size_Medium_Option:') + 19:line.find('Size_Medium_Option:') + 20]))
        if (line.find('Size_Small_Option:') == 0):
            Checkbutton(ws, text="Small" , variable=Small, onvalue=1, offvalue=0, command=SmallIsChecked).place(x=205,y=150)
            Small.set(int(line[line.find('Size_Small_Option:') + 18:line.find('Size_Small_Option:') + 19]))
    file.close()

    AutoCorrectbtn = Button(ws, text='AutoCorrect', padx=40, pady=5,command=Correct).place(x=10,y=200)
    ForceStopbtn   = Button(ws, text='ForceStop', padx=40, pady=5, command=ForceStop).place(x=210,y=200)
    Executebtn     = Button(ws, text='Execute', padx=147, pady=5,command=Execute).place(x=10,y=250)

    ws.mainloop()
