"""
User management system

The User management system is an application 
to customize the preferences of a Human Activity Recognition System.
It is designed to work with the Office Hydration Monitoring (OHM) Dataset
(https://zenodo.org/record/4681206).
It includes several options to customize the system:

- Name: Defined preferences will be associated with each user name
- Desired level of participation in the proposed interactive scenario:
Three levels of involvement are defined: None, Low, Intermediate or High. This
selection determines the number of times the IoT device may ask the user
about a specific activity performed.
- Classification mode: This is specific for the OHM Dataset. It allows defining 
whether the user wants the system to discern between the type of
container used: Bottle or Cup/Mug or not.


When cliking "Update preferences" button, those are saved in "preferences.json"
in the format:

{
    "Name": "", 
    "Involvement": "", 
    "Class_type": ""
}

"""


import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import os
import pyqtgraph.console
import PyQt5
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QMenu, QSlider
from PyQt5.QtGui import QLineEdit, QFont
from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json

#Variables
data_global=""
Activity="Drink / Other"
Subject="Unknown"
classification_type = ""
save= False
data_global=""

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








"""
User name definition
"""
#Save introduced user name variable
def on_click():
    global Subject
    textboxValue = textbox.text()
    Subject=textboxValue
    print("Name changed to: "+str(Subject)+'\n')
    textboxValue=""
    
#Save introduced user name variable      
def selection_change():
	global Activity
	Activity=btn4.currentText()
	print ((tranformActivity(Activity)))

"""
Participation level
"""
#Slider funtionality
def SliderchangedValue():
    global slider_value
    global value
    value = slider.value()
    slider_value = translateSlider(value)
    print(slider_value)
    return slider_value


#Print a description of every participation level when scrolling    
def translateSlider(slider_value):
	slider_translated = ""
	if slider_value == 0:
		slider_translated = "None participation level:\nThe system will never inquire you about a detected activity\n"
	elif slider_value == 1:
		slider_translated = "Low participation level: \nThe system may inquire you about a detected activity\n"
	elif slider_value == 2:
		slider_translated = "Medium participation level: \nThe system is more likely to inquire you about a detected activity\n"
	elif slider_value == 3:
		slider_translated = "High participation level: \nThe system will frequently inquire you about a detected activity\n"
	return slider_translated

#Associate the participation selection with the saved preference
def translateSliderShort(slider_value):
	slider_translated_short = ""
	if slider_value == 0:
		slider_translated_short = "None participation level"
	elif slider_value == 1:
		slider_translated_short = "Low participation level"
	elif slider_value == 2:
		slider_translated_short = "Medium participation level"
	elif slider_value == 3:
		slider_translated_short = "High participation level"
	return slider_translated_short


"""
Classification mode
"""
#Save the classification mode
def tranformActivity(Activity):

	global classification_type
	if Activity == "Drink / Other":
		classification_type= "\nDrink / Other: The system will only differentiate drinking activity over the rest of movements\n"
	if Activity == "Drink Bottle / Drink Mug / Other":
		classification_type= "\nDrink Bottle / Drink Mug / Other: The system will differentiate both drinking activity over the rest of movements and the kind of container used\n "
	return classification_type

def tranformActivityShort(Activity):
	global classification_type
	if Activity == "Drink / Other":
		classification_type= "Drink / Other"
	if Activity == "Drink Bottle / Drink Mug / Other":
		classification_type= "Drink Bottle / Drink Mug / Other"
	return classification_type


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
Save preferences
"""
#Save preferences with "Update preferences" button
def clicked():
    #Print selection
    print("\n \n ")
    print("----------------------------------------------")
    print("Your new preferences are:\n")
    print("Name:")
    print(str(Subject)+"\n")
    print("Imvolvement level:")
    print(str(translateSliderShort(value))+"\n")
    print("Classification Type:")
    print(tranformActivityShort(Activity))
    print("----------------------------------------------")
    print("\n \n ")

    #Save preferences Json
    keyList = ["Name", "Involvement", "Class_type"] 
    saveDict = {key: None for key in keyList} 
    saveDict["Name"] = Subject
    saveDict["Involvement"] = translateSliderShort(value)
    saveDict["Class_type"] = tranformActivityShort(Activity)
    with open('preferences.json', 'w') as fp:
         json.dump(saveDict, fp)

"""
Quit application. Close window
"""
#Quit button
def Quit():
    win.close()




#-----------------------------
#-------- Interface ----------
#-----------------------------


#Set window interface configuration and inizialize Qt
pg.setConfigOption('background','w')
pg.setConfigOption('background',QtGui.QColor(231,231,231))
app = QtGui.QApplication([])
app.setStyle('Fusion')

#Create app layout
w = QtGui.QWidget()
w.setWindowTitle('User Management System - Set preferences')
win = pg.GraphicsWindow()
win.setWindowTitle('User Management System - Set preferences')
layout1 = QtGui.QGridLayout()
win.setLayout(layout1)
win.resize(150,900)


## Create buttons and widgets
#Define buttons funtionality

#User name
nameLabel = QLabel()
nameLabel.setText('Insert your name:')
with open('preferences.json', 'r') as fp: #Load prreviously saved preferences
    data = json.load(fp)
textbox = QLineEdit(data["Name"])
BtnText = QPushButton('Save Name')
BtnText.clicked.connect(on_click)
BtnText.setStyleSheet("background-color: #028090; color: white")
BtnText.setFont(QFont("Arial", 15))
textbox.setFont(QFont("Arial", 15))

#Combobox classification mode options
btn4 = QtGui.QComboBox()  
btn4.addItem("Drink / Other")
btn4.addItem("Drink Bottle / Drink Mug / Other")                                                                                                                                          
btn4.activated.connect(selection_change)
btn4.setStyleSheet("background-color: #028090; color: white")
btn4.setFont(QFont("Arial", 20))

#Update preferences
btn1 = QtGui.QPushButton('Update Preferences')
btn1.clicked.connect(clicked)
btn1.setStyleSheet("background-color: #00a896; color: white;height: 2px;width: 2px;")
btn1.setFont(QFont("Arial", 20))

#Quit app
btn2 = QtGui.QPushButton('Quit')
btn2.clicked.connect(Quit)
btn2.setStyleSheet("background-color: red; color: white")
btn2.setFont(QFont("Arial", 20))

#Text
nameLabel0 = QLabel()
nameLabel0.setText('')
nameLabel5 = QLabel()
nameLabel5.setText('')
nameLabel6 = QLabel()
nameLabel6.setText(' Select the classification mode: ')
nameLabel7 = QLabel()
nameLabel7.setText('')


#Slider
grid_slider = QGridLayout()
slider = QSlider(Qt.Horizontal)
slider.setFocusPolicy(Qt.StrongFocus)
slider.setTickPosition(QSlider.TicksBothSides)
slider.setMinimum(0)
slider.setMaximum(3)
slider.setTickInterval(1)
slider.setSingleStep(3)
slider.setFocusPolicy(Qt.NoFocus)
nameLabel3 = QLabel()
nameLabel3.setText('\nSelect your desired participation level:')
slider.valueChanged.connect(SliderchangedValue)
nameLabel4 = QLabel()
nameLabel4.setText('None              Low            Intermediate       High')
slider.setStyleSheet("QSlider::groove:horizontal { "
                      "height: 12px; "
                      "background: #05668d1; "
                      "margin: 2px 0; "
                      "} "
                      "QSlider::handle:horizontal { "
                      "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f); "
                      "border: 1px solid #5c5c5c; "
                      "width: 30px; "
                      "margin: -2px 0px; "
                      "} ")


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
    "-" * 65 + '\n' + "                            Activity Log       " + '\n' + "-" * 65 + "\n" )



nameLabel0.setFont(QFont("Arial", 4))
nameLabel.setFont(QFont("Arial", 16, QtGui.QFont.Bold))
nameLabel3.setFont(QFont("Arial", 16, QtGui.QFont.Bold))
nameLabel4.setFont(QFont("Arial", 15))
nameLabel5.setFont(QFont("Arial", 15))
nameLabel6.setFont(QFont("Arial", 16, QtGui.QFont.Bold))
nameLabel7.setFont(QFont("Arial", 15))


#Define layout
layout = QtGui.QGridLayout()
win.setLayout(layout)
layout1.addWidget(nameLabel, 0, 0)
layout1.addWidget(textbox, 1, 0)
layout1.addWidget(BtnText, 2, 0)
BtnText.setFixedWidth(win.width()/1.05)

#Slider
layout1.addWidget(nameLabel3, 3, 0)
layout1.addWidget(nameLabel0, 4, 0)
layout1.addWidget(nameLabel4, 5, 0)
layout1.addWidget(slider, 6, 0)
layout1.addWidget(nameLabel5, 7, 0)

#Select Mode
layout1.addWidget(nameLabel6, 8, 0)
layout1.addWidget(btn4, 9, 0) # button goes in upper-left
btn4.setFixedHeight(win.height()/20)
layout1.addWidget(nameLabel7, 10, 0)

#Terminal
layout1.addWidget(listw, 11, 0) # list widget goes in bottom-left

#Save
layout1.addWidget(btn1, 12, 0)
btn1.setFixedHeight(win.height()/20)
#Out
layout1.addWidget(btn2, 13, 0)
btn2.setFixedHeight(win.height()/20)

btn1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
btn2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
listw.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


## Display the widget as a new window
win.show()


## Qt event loop 
if __name__ == '__main__':
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                QtGui.QApplication.instance().exec_()

        
        

            
