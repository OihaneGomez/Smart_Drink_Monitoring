"""
Model personalization engine

The Model personalization engine is an application designed to help users
in the process of personalizing Human Activity Recognition models. 
Its interface allows them to easily and visually provide examples of their 
own movement patterns.

It was designed to work with M5Stick-C device, capturing Accelerometer, 
Gyroscope and Pitch, Roll and Yaw signals. Only AccX, AccY and AccZ signals 
will be displayed through the interfacte.

IoT devices are connected via Bluetooth. Thus, the MAC address 
of the device is needed. This device has to be accessible when running this 
application. Otherwise it wont load the interface

"""


import serial
import time
import numpy as np
from matplotlib import pyplot as plt
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import os
import pyqtgraph.console
import PyQt5
import sys
from bluepy.btle import *
import struct
from functools import reduce
from PyQt5 import QtWidgets
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QMenu, QSlider
from PyQt5.QtGui import QLineEdit, QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from datetime import datetime
import json


# -------------------- Device MAC ADDRESS
device_mac = "" #Add the mac adress of the device you want to connect
# --------------------




#Variables
data_global=""
Activity="Drink"
Subject="Unknown"
save= False
data_global=""
preValue=0.0
slider_value = 0
preValue=0.0
i =0 
control_gui=""
pause = False
mode = "Drink / Other"



#Color format
palette = QtGui.QPalette()
palette.setColor(QtGui.QPalette.Window, QtGui.QColor(112,115,116))
palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)





#---------------------------------------
#-------- Funtion definitions ----------
#---------------------------------------

"""
Activity log
"""
#Print activity log
class Port(object):
    def __init__(self, view):
        self.view = view

    def flush(self):
        pass

    def write(self, text):
        cursor = self.view.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.view.setTextCursor(cursor)
        self.view.ensureCursorVisible()

"""
Obtain and check signals
"""
class DataView:
    def __init__(self, array, bytes_per_element=1):
        self.array = array
        self.bytes_per_element = 1
    def __get_binary(self, start_index, byte_count, signed=False):
        integers = [self.array[start_index + x] for x in range(byte_count)]
        bytes = [integer.to_bytes(self.bytes_per_element, byteorder='little', signed=signed) for integer in integers]
        return reduce(lambda a, b: a + b, bytes)
        
    def get_float_32(self, start_index):
        bytes_to_read = 4
        binary = self.__get_binary(start_index, bytes_to_read)
        return struct.unpack('<f', binary)[0] # <f for little endian
        
    
def arrayisfloat(array):
        try:
                global preValue 
                value = [float(i.strip()) for i in array]
                preValue = value
                return value
        except ValueError:
                print ("---------Not a float" + str(array))
                value = preValue
                return value



"""
Define activity
"""
def selectionchange():
   global Activity
   Activity=btn4.currentText()
   print ("Activity: ",btn4.currentText())
   

   
"""
Play/pause data aquisition
"""                 
def clicked():
    global pause
    global save
    global control_gui
    if(pause):
        QtGui.QLineEdit.setText(text,'Pause')
        control_gui="stop"
    else:
        QtGui.QLineEdit.setText(text,'Running on MCU...')
        control_gui="start"
    pause = not(pause)    
    

"""
Get current time to add it to file name
"""      
def get_time():
    now = datetime.now()
    time = now.strftime("%d-%m-%Y_%H-%M-%S")
    return time


"""
Save captured data in txt file.
"""        
def clickedSave():
    global Activity
    global data1
    data_save = []                  
    edge = lr11.getRegion()
    edge = (int(edge[0]),int(edge[1]))
    data_save = data1[:,edge[0]:edge[1]]
    data_save= data_save.transpose()
    path = os.path.join(('Data'+"/"+str(Activity)))
    if not os.path.exists(path):
        os.makedirs(path)
    f = path+"/"+str(Activity)+"_"+str(Subject)+"_"+str(get_time())+".txt"
    np.savetxt(f,data_save,fmt='%10.9f',newline='\n',delimiter = ',',)         
    print("Data saved as:")
    Activity=Activity.replace(" ", "_");
    print(str(Activity)+"_"+str(Subject)+"_"+str(get_time())+".txt \n")
    print("Your personalized model will be updated with the new data! \n \n")


      
"""
Quit application. Close window
"""
def Quit():
    w.close()


k = 1   
 

#---------------------------------------------------
#-------- BLE connection and data capture ----------
#---------------------------------------------------
 
class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global data_global #Global variable to store recieved data (X Y Z)
        if data is not None:
            d = DataView(data)
            x=d.get_float_32(0)
            y=d.get_float_32(4)
            z=d.get_float_32(8)
            
            data_global=np.array([x,y,z])

            
            
            #data_global = str(data.decode(encoding = 'UTF-8'))
            
            #print ("Notification    " + str(data_global))
        
    def update(self):
        global data, data1, curve11, curve21, curve31, save, f, pause, control_gui, Subject, data_global, Activity
        #Pause button
        if per.waitForNotifications(0.05):
            try:
                if data_global is not None:
                    if (control_gui=="start"):
                        print("\n----  Start recording----\n Perfom now the selected activity and press Star/Stop one finished\n\n" )
                        control_gui=""
                        path = os.path.join(('Data'+"/"+str(Activity)))
                        if not os.path.exists(path):
                            os.makedirs(path)
                    
                        #create initial file 
                        f = open(path+"/"+str(Activity)+"_"+str(Subject)+"_"+str(get_time())+".txt",'a')
                        #saving data only when start button was pressed once
                        if not save:
                            save=not save
                        
                    elif (control_gui=="stop"):
                        
                        print("----  Stop ---- \n Recording Stopped, you can now crop the signal and save the new data\n\n")
                        if save:
                            f.close()
                            control_gui = "iddle"
                            
                    elif (control_gui=="iddle"):
                        acc=[]
                    else:
                        tab = [float(i) for i in data_global]
                        acc = tab[0:9] #read and store the 9 values
                        acc = "," .join(map(str, acc))
                        
                        #saving data only when start button was pressed once
                        if save:
                            f.writelines(str(acc)+"\n")
                            tps[:-1] = tps[1:]
                            tps[-1] = time.time()-start
                            data1[:,:-1] = data1[:,1:]  # shift data in the array one sample left 
                            data1[:,-1] = data_global
                            curve11.setData(data1[0])
                            curve21.setData(data1[1])
                            curve31.setData(data1[2]) 
                            #saving data only when start button was pressed once
                            #if save:
                                #f.writelines(str(i) for i in acc+"\n")

            except KeyboardInterrupt:
                  print ('Finished')
                  sys.exit()
                  w.close()               
                
tps = np.zeros(3000) 




#-----------------------------
#-------- Interface ----------
#-----------------------------


#Set windows interface configuration and inizialize Qt
sys.tracebacklimit=None
#Set window interface configuration
pg.setConfigOption('background','w')
pg.setConfigOption('background',QtGui.QColor(50,50,50))
app = QtGui.QApplication([])
app.setStyle('Fusion')

#Create app layout
w = QtGui.QWidget()
w.setWindowTitle('User Management System - Model Personalization Engine')
wb = QtGui.QWidget(w)
win = pg.GraphicsWindow()
win.setWindowTitle('Model Personalization Engine')
win.resize(1366,1100)

## Create buttons and widgets
#Define buttons funtionality

#Instructions
nameLabel = QLabel()
nameLabel.setText('INSTRUCTIONS:\n\n1 - Press the central button of the device \nfor 5 second to enter in annotation mode \n')
nameLabel2 = QLabel()
nameLabel2.setText('2 - Select the activity you want to record')
textbox = QLineEdit('')

#Select activity combo box
#Options will depend on the classification model selected in the User Management System
with open('preferences.json', 'r') as fp: #Read preferences json file
    data = json.load(fp)
    mode = data["Class_type"]
    Subject = data["Name"]
if mode == "Drink / Other": #Define available options
    item_list = ['Drink', 'Other']
                                                                                
if mode == "Drink Bottle / Drink Mug / Other":
    item_list = ['Drink Bottle', 'Drink Mug', 'Other']
btn4 = comboBox = QtGui.QComboBox()     
comboBox.addItems(item_list)
btn4.activated.connect(selectionchange)
btn4.setStyleSheet("background-color: #028090; color: white")
btn4.setFont(QFont("Arial", 20))
btn4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
text = QtGui.QLineEdit()

#Start/Stop button
nameLabel3 = QLabel()
nameLabel3.setText('\n3 - Push "Start/Stop" button to start')
btn3 = QtGui.QPushButton('Start/Stop')
btn3.clicked.connect(clicked)
btn3.setStyleSheet("background-color: #028090; color: white")
btn3.setFont(QFont("Arial", 20))


#Instructions
nameLabel4 = QLabel()
nameLabel4.setText('\n4 - Perform the selected activity once \nand stop the recording\n\n5- Crop the signal and click "Save Data" ')
nameLabel5 = QLabel()
nameLabel5.setText('\n5 - Press the right button of the device \n5 second to leave annotation mode\n')

#Save data button
btn1 = QtGui.QPushButton('Save Data')
btn1.clicked.connect(clickedSave)
btn1.setStyleSheet("background-color: #00a896; color: white;height: 2px;width: 2px;")
btn1.setFont(QFont("Arial", 20))
btn1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



# Log OutPut
listw = QtWidgets.QTextBrowser()
sys.stdout = Port(listw)

listw.setStyleSheet(
            """QTextBrowser {background-color:  #F8F9FA;
                               color: #000000;
                               font: 13pt Arial;
                               width: 20px;
height: 20px;}""")

listw.document().setPlainText(
    "-" * 50 + '\n' + "                     Activity Log       " + '\n' + "-" * 50 + "\n\n")


#Exit button
btn2 = QtGui.QPushButton('Quit')
btn2.clicked.connect(Quit)
btn2.setStyleSheet("background-color: red; color: white")
btn2.setFont(QFont("Arial", 20))
btn2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



nameLabel.setFont(QFont("Arial", 15))
nameLabel2.setFont(QFont("Arial", 15))
nameLabel3.setFont(QFont("Arial", 15))
nameLabel4.setFont(QFont("Arial", 15))
nameLabel5.setFont(QFont("Arial", 15))
textbox.setFont(QFont("Arial", 15))



#Define layout 
layout = QtGui.QGridLayout()
wb.setLayout(layout)
wb.setFixedWidth(w.width()/1.7)
layout1 = QtGui.QGridLayout()
w.setLayout(layout1)


## Add widgets
layout.addWidget(nameLabel, 1, 0)#instructions

layout.addWidget(nameLabel2,4, 0) #instructions

layout.addWidget(btn4, 5, 0) #Select activity combo box
btn4.setFixedHeight(w.height()/10)

layout.addWidget(nameLabel3, 6, 0)#instructions

layout.addWidget(btn3, 7, 0) #Start/Stop button
btn3.setFixedHeight(w.height()/10)

layout.addWidget(nameLabel4, 8, 0)#instructions

layout.addWidget(btn1, 9, 0)#Save data button
btn1.setFixedHeight(w.height()/10)

layout.addWidget(listw, 10, 0) #Log

layout.addWidget(nameLabel5, 11, 0)#instructions

layout.addWidget(btn2, 12, 0)#Exit button
btn2.setFixedHeight(w.height()/10)#Exit button

layout1.addWidget(wb, 0,0)# Signal plot
layout1.addWidget(win, 0,1)


## Display the widget as a new window
w.showMaximized()
win.setFrameStyle(2)


## Signal Plot regions

def regionUpdated(regionItem):
    lo,hi =regionItem.getRegion()
    lr11.setRegion([lo,hi])
    lr21.setRegion([lo,hi])
    lr31.setRegion([lo,hi])

#Define a section for each plot
lo=20
hi=100

lr11 = pg.LinearRegionItem(values= [lo,hi]) #X
lr21 = pg.LinearRegionItem(values= [lo,hi]) #X
lr31 = pg.LinearRegionItem(values= [lo,hi]) #X
lr11.sigRegionChanged.connect(regionUpdated)
lr21.sigRegionChanged.connect(regionUpdated)
lr31.sigRegionChanged.connect(regionUpdated)


data1 = np.zeros((3,250)); #contains acc_x, acc_y and acc_z 

#Plot 1 - X
p11 = win.addPlot()
p11.addLegend(offset=(10,10))
p11.addItem(lr11,name='region11')
win.nextRow()

#Plot 2 - Y
p21 = win.addPlot()
p21.addLegend(offset=(10,10))
p21.addItem(lr21,name='region21')
win.nextRow()

#Plot 3 - Z
p31 = win.addPlot()
p31.addLegend(offset=(10,10))
p31.addItem(lr31,name='region31')

#Define X,Y,Z Signas
curve11 = p11.plot(data1[0],pen="w",name = 'Accelerometer X')
curve21 = p21.plot(data1[1],pen="r",name = 'Accelerometer Y')
curve31 = p31.plot(data1[2],pen="g",name = 'Accelerometer Z')



#Define cursor
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p11.addItem(vLine, ignoreBounds=True)
p11.addItem(hLine, ignoreBounds=True)

vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p21.addItem(vLine, ignoreBounds=True)
p21.addItem(hLine, ignoreBounds=True)

vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p31.addItem(vLine, ignoreBounds=True)
p31.addItem(hLine, ignoreBounds=True)


# ----------------------------------------------------------------------------------
# Connect BLE: add MAC address
#----------------------------------------------------------------------------------


try:
    per = Peripheral(device_mac, "public")
    per.setDelegate(MyDelegate())
    #Read characteristic data
    notify = per.getCharacteristics(uuid='6e400003-b5a3-f393-e0a9-e50e24dcca9e')[0]

    # enable notification
    setup_data = b"\x01\x00"
    notify_handle = notify.getHandle() + 1
    per.writeCharacteristic(notify_handle, setup_data, withResponse=True)

    # send test string
    c = per.getCharacteristics(uuid='6e400002-b5a3-f393-e0a9-e50e24dcca9e')[0]
    callback="Conected"
    c.write(callback.encode("utf-8"))

    #Class Instance to user update() later
    delegate_instance=MyDelegate()

    start = time.time()
    timer = pg.QtCore.QTimer()
    #Call update method
    timer.timeout.connect(delegate_instance.update)
    timer.start(5)

except BTLEException as e:
    print ("BLE Exception in scan:", e)

# --------------------------------------------------------------------------------



## Qt event loop 
if __name__ == '__main__':
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                QtGui.QApplication.instance().exec_()

        

        

            
