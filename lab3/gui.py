# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import paho.mqtt.client as mqtt
import json
import time


class Ui_MainWindow(object):
    updateParkingSignal = QtCore.pyqtSignal(list)
    updateTemperatureSignal  = QtCore.pyqtSignal(float)
    updateEmergencySignalOn = QtCore.pyqtSignal(bool)
    updateEmergencySignalOff = QtCore.pyqtSignal(bool)
    updateEmergencyLightSignal = QtCore.pyqtSignal(str)
    broker = 'mqtt.eclipseprojects.io'
    client = mqtt.Client("gui_ruiz")
    spots = []
    client.connect(broker)
    emergencyStatus = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(962, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.parkingFrame = QtWidgets.QFrame(self.centralwidget)
        self.parkingFrame.setGeometry(QtCore.QRect(20, 20, 920, 100))
        self.parkingFrame.setStyleSheet("border: 1px solid black;")
        self.parkingFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.parkingFrame.setObjectName("parkingFrame")
        self.parkingLayout = QtWidgets.QHBoxLayout(self.parkingFrame)

        for i in range(1, 6):
            parkingSpot = QtWidgets.QLabel(self.parkingFrame)
            parkingSpot.setStyleSheet("background-color: red; border: 1px solid black;")
            parkingSpot.setAlignment(QtCore.Qt.AlignCenter)
            parkingSpot.setObjectName(f"parking{i}")
            parkingSpot.setText(str(i))
            self.parkingLayout.addWidget(parkingSpot)
            setattr(self, f'parking{i}', parkingSpot)

        self.spots.extend([self.parking1, self.parking2, self.parking3, self.parking4, self.parking5])

        self.controlsLayout = QtWidgets.QHBoxLayout()

        self.tempFrame = QtWidgets.QFrame(self.centralwidget)
        self.tempFrame.setStyleSheet("border: 1px solid black;")
        self.tempFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tempLayout = QtWidgets.QVBoxLayout(self.tempFrame)
        self.tempSensorLabel = QtWidgets.QLabel("Temperature Sensor", self.tempFrame)
        self.tempSensorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tempSensorLabel.setStyleSheet("padding: 10px;")
        self.tempLayout.addWidget(self.tempSensorLabel)
        self.tempSensorValueLabel = QtWidgets.QLabel("Placeholder", self.tempFrame)
        self.tempSensorValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.tempSensorValueLabel.setStyleSheet("padding: 10px;")
        self.tempLayout.addWidget(self.tempSensorValueLabel)
        self.controlsLayout.addWidget(self.tempFrame)

        self.emergencyFrame = QtWidgets.QFrame(self.centralwidget)
        self.emergencyFrame.setStyleSheet("border: 1px solid black;")
        self.emergencyFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.emergencyLayout = QtWidgets.QVBoxLayout(self.emergencyFrame)
        self.emergencyLabel = QtWidgets.QLabel(self.emergencyFrame)
        self.emergencyLabel.setObjectName("emergencyLabel")
        self.emergencyLabel.setStyleSheet("""
            QLabel {
                background-color: gray;
                border: 2px solid black;
                border-radius: 25px;  /* Adjust this value to half of your QLabel's width and height to make it circular */
            }
        """)
        self.emergencyLabel.setMinimumSize(50, 50)
        self.emergencyLabel.setMaximumSize(50, 50)
        self.emergencyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.emergencyLayout.addWidget(self.emergencyLabel)
        self.controlsLayout.addWidget(self.emergencyFrame)
        self.emergencyOffButton = QtWidgets.QPushButton("Emergency Off", self.emergencyFrame)
        self.emergencyOffButton.clicked.connect(self.updateEmergencyStatusOff)
        self.emergencyOffButton.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #c0c0c0;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #007bff;
                color: white;
            }
            QPushButton:pressed {
                background-color:
                border-style: inset;
            }
        """)
        self.emergencyLayout.addWidget(self.emergencyOffButton)
        self.emergencyOnButton = QtWidgets.QPushButton("Emergency On", self.emergencyFrame)
        self.emergencyOnButton.clicked.connect(self.updateEmergencyStatusOn)
        self.emergencyOnButton.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #c0c0c0;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #007bff;
                color: white;
            }
            QPushButton:pressed {
                background-color:
                border-style: inset;
            }
        """)
        self.emergencyLayout.addWidget(self.emergencyOnButton)
        spacerLeft = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerRight = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.emergencyLayout.addSpacerItem(spacerLeft)
        self.emergencyLayout.addWidget(self.emergencyLabel, 0, QtCore.Qt.AlignCenter)
        self.emergencyLayout.addSpacerItem(spacerRight)

        self.messageBoardFrame = QtWidgets.QFrame(self.centralwidget)
        self.messageBoardFrame.setGeometry(QtCore.QRect(20, 240, 920, 150))
        self.messageBoardFrame.setStyleSheet("border: 1px solid black;")
        self.messageBoardFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.messageBoardLayout = QtWidgets.QVBoxLayout(self.messageBoardFrame)
        self.messageboardLabel = QtWidgets.QLabel("Display message to display board", self.messageBoardFrame)
        self.messageboardLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.messageBoardLayout.addWidget(self.messageboardLabel)
        self.messageBoardInput = QtWidgets.QTextEdit(self.messageBoardFrame)
        self.messageBoardLayout.addWidget(self.messageBoardInput)
        self.messageBoardSend = QtWidgets.QPushButton("Display", self.messageBoardFrame)
        self.messageBoardSend.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #c0c0c0;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #007bff;
                color: white;
            }
            QPushButton:pressed {
                background-color:
                border-style: inset;
            }
        """)
        self.messageBoardSend.clicked.connect(self.sendBoardMessage)
        self.messageBoardLayout.addWidget(self.messageBoardSend)

        self.centralLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.centralLayout.addWidget(self.parkingFrame)
        self.centralLayout.addLayout(self.controlsLayout)
        self.centralLayout.addWidget(self.messageBoardFrame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.emergencyThread = threading.Thread(target=self.handleEmergency)
        self.emergencyThread.daemon = True
        self.emergencyThread.start()

        self.updateParkingSignal.connect(self.updateParking)
        self.updateTemperatureSignal.connect(self.updateTemperature)
        self.updateEmergencySignalOn.connect(self.updateEmergencyStatusOn)
        self.updateEmergencySignalOff.connect(self.updateEmergencyStatusOff)
        self.updateEmergencyLightSignal.connect(self.updateEmergencyLight)
        self.client.connect(self.broker)
        self.client.loop_start()
        self.client.subscribe("parking_ruiz")
        self.client.subscribe("temperature_ruiz")
        self.client.on_message = self.on_message

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.messageboardLabel.setText(_translate("MainWindow", "Send message to display board"))
        self.messageBoardInput.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.messageBoardInput.setPlaceholderText(_translate("MainWindow", "Type message here"))
        self.messageBoardSend.setText(_translate("MainWindow", "Send"))
        self.parking1.setText(_translate("MainWindow", "1"))
        self.parking2.setText(_translate("MainWindow", "2"))
        self.parking3.setText(_translate("MainWindow", "3"))
        self.parking4.setText(_translate("MainWindow", "4"))
        self.parking5.setText(_translate("MainWindow", "5"))
        self.tempSensorLabel.setText(_translate("MainWindow", "Temperature Sensor"))
        self.tempSensorValueLabel.setText(_translate("MainWindow", ""))
        self.emergencyOffButton.setText(_translate("MainWindow", "Turn Emergency Light Off"))
        self.emergencyOnButton.setText(_translate("MainWindow", "Turn Emergency Light On"))

    def sendBoardMessage(self):
        try:
            raw = {
                "type":"msg_board",
                "data":self.messageBoardInput.toPlainText()
			}
            payload = json.dumps(raw)
            self.client.publish("MSG_BOARD", payload)
            print("[MSG BOARD] Just published %s to topic \"MSG_BOARD\"" % payload)
        except Exception as e:
             print(f'[MSG BOARD] {e}') 

    def updateParking(self, parking):
        for i in range(0, len(parking)):
            if parking[i]:
                self.spots[i].setStyleSheet("background-color: green; border: 1px solid black;")
            else:
                self.spots[i].setStyleSheet("background-color: red; border: 1px solid black;")

                
    def updateTemperature(self, temp):
        result = round(temp, 2)
        self.tempSensorValueLabel.setText(str(result) + " o C")
                
    def on_message(self, client, userdata, message):
        try: 
            payload = json.loads(message.payload)
            type = payload["type"]
            data = payload["data"]
            print(f"[{type}] Received message: {str(data)}")
            if type == "parking":
                self.updateParkingSignal.emit(data)
            if type == "temperature":
                self.updateTemperatureSignal.emit(data)
        except Exception as e:
            print(f"Error processing message: {e}")

    def updateEmergencyStatusOn(self):
        self.emergencyStatus = True 
        self.sendEmergencySignal(True)

    def updateEmergencyStatusOff(self):
        self.emergencyStatus = False
        self.sendEmergencySignal(False)
    

    def sendEmergencySignal(self, status):
        try:
            raw = {
                "type":"emergency",
                "data":status
			}
            payload = json.dumps(raw)
            self.client.publish("emergency", payload)
            print("[emergency] Just published %s to topic \"emergency\"" % payload)
        except Exception as e:
             print(f'[emergency] {e}')   

    def handleEmergency(self):
        while True:
            if self.emergencyStatus:
                self.updateEmergencyLightSignal.emit("red")
                time.sleep(0.25)
                self.updateEmergencyLightSignal.emit("blue")
                time.sleep(0.25)
            else:
                self.updateEmergencyLightSignal.emit("gray")
    
    def updateEmergencyLight(self, color):
        stylesheet = f"""
            QLabel {{
                background-color: {color};
                border: 2px solid black;
                border-radius: 25px;
            }}
        """
        self.emergencyLabel.setStyleSheet(stylesheet)

class emergencyLightGraphic(QtWidgets.QWidget):
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        painter.drawEllipse(160,0,50, 50)



class MyApplication(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyApplication()
    mainWindow.show()
    sys.exit(app.exec_())