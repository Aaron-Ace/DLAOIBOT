from tkinter import *
import cv2
import serial
import sys
from main_choice import mainfunc

def ScrewIsChecked():
    pass
    '''if Screw.get() == 1:
        file = open("OptionCheckList.ini", "w")
        count = 0
        for line in file:
            if (count == 0):
                line = "Screw_Option:1"
            count += 1
        file.close()
    elif Screw.get() == 0:
        file = open("OptionCheckList.ini", "w")
        count = 0
        for line in file:
            if (count == 0):
                line = "Screw_Option:0"
            count += 1
        file.close()
    else:
        messagebox.showerror('PythonGuides', 'Something went wrong!')'''

def NutIsChecked():
    pass

def BigIsChecked():
    pass

def MidIsChecked():
    pass

def SmallIsChecked():
    pass

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



def ForceStop():
    sys.exit()
def Execute():
    mainfunc()
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


    Screw = IntVar()
    Nut   = IntVar()
    Big   = IntVar()
    Mid   = IntVar()
    Small = IntVar()
    Checkbutton(ws, text="Screw" , variable=Screw, onvalue=1, offvalue=0, command=ScrewIsChecked()).place(x=5,y=100)
    Checkbutton(ws, text=" Nut " , variable=Nut  , onvalue=1, offvalue=0, command=NutIsChecked()).place(x=105,y=100)
    Checkbutton(ws, text=" Big " , variable=Big  , onvalue=1, offvalue=0, command=BigIsChecked()).place(x=5,y=150)
    Checkbutton(ws, text="Medium", variable=Mid  , onvalue=1, offvalue=0, command=MidIsChecked()).place(x=105,y=150)
    Checkbutton(ws, text="Small" , variable=Small, onvalue=1, offvalue=0, command=SmallIsChecked()).place(x=205,y=150)

    file = open('OptionCheckList.ini', 'r')
    log = []
    for line in file:
        if (line.find('Screw_Option:') != -1):
            Screw = int(line[line.find('Screw_Option:') + 13:line.find('Screw_Option:') + 14])
        if (line.find('Nut_Option:') != -1):
            Nut = int(line[line.find('Nut_Option:') + 11:line.find('Nut_Option:') + 12])
        if (line.find('Size_Big_Option:') != -1):
            Big = int(line[line.find('Size_Big_Option:') + 16:line.find('Size_Big_Option:') + 17])
        if (line.find('Size_Medium_Option:') != -1):
            Mid = int(line[line.find('Size_Medium_Option:') + 19:line.find('Size_Medium_Option:') + 20])
        if (line.find('Size_Small_Option:') != -1):
            Small = int(line[line.find('Size_Small_Option:') + 18:line.find('Size_Small_Option:') + 19])
    file.close()

    AutoCorrectbtn = Button(ws, text='AutoCorrect', padx=40, pady=5).place(x=10,y=200)
    ForceStopbtn   = Button(ws, text='ForceStop', padx=40, pady=5, command=ForceStop).place(x=210,y=200)
    Executebtn     = Button(ws, text='Execute', padx=147, pady=5,command=Execute).place(x=10,y=250)

    ws.mainloop()