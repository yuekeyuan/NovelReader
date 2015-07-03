#coding=utf-8
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QPalette
import json, os, sys
class MainUI(QtGui.QWidget):
    config = None
    def __init__(self, parent = None):
        super(MainUI, self).__init__(parent, QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.preInitConfig()
        self.initConfigInfo()
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.config["mainUi"]["width"], self.config["mainUi"]["height"])
        self.createHeader()
        self.createBody()
        self.createHeader()
        self.createFooter()
        self.header.move(0,0)
        self.body.move(self.config["mainUi"]["head"]["x"], self.config["mainUi"]["head"]["y"])
        self.footer.move(self.config["mainUi"]["foot"]["x"], self.config["mainUi"]["foot"]["y"])
    def preInitConfig(self):
        f = open("config.json", "r")
        self.config = json.load(f)

        if "preInit" in self.config and self.config["preInit"] == "false":
            self.config["preInit"] = "true"
            #deskTop
            deskTop = QtGui.QApplication.desktop()
            self.config["deskTop"]["width"] = deskTop.size().width()
            self.config["deskTop"]["height"] = deskTop.size().height()
            #mainUi
            self.config["mainUi"]["x"] = 0
            self.config["mainUi"]["y"] = 0
            self.config["mainUi"]["width"] = int(self.config["deskTop"]["width"] /2 )
            self.config["mainUi"]["height"] = int(self.config["deskTop"]["height"] / 2)
            #head
            self.config["mainUi"]["head"]["x"] = 0
            self.config["mainUi"]["head"]["y"] = 0
            self.config["mainUi"]["head"]["width"] = self.config["mainUi"]["width"]
            self.config["mainUi"]["head"]["height"] = 30
            #foot
            self.config["mainUi"]["foot"]["x"] = 0
            self.config["mainUi"]["foot"]["y"] = self.config["mainUi"]["height"] - self.config["mainUi"]["foot"]["height"]
            self.config["mainUi"]["foot"]["width"] = self.config["mainUi"]["head"]["width"]
            self.config["mainUi"]["foot"]["height"] = self.config["mainUi"]["head"]["height"]
        f.close()
        f = open("config.json", "w")
        json.dump(self.config, f, indent=4)
        f.close()

    def initConfigInfo(self):
        f = open("config.json", "r")
        self.config = json.load(f)
        f.close()

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(self.config["mainUi"]["background-color"][0],\
            self.config["mainUi"]["background-color"][1],\
            self.config["mainUi"]["background-color"][2],\
            self.config["mainUi"]["background-color"][3])
        painter.fillRect(self.rect(), color)

    def createHeader(self):
        self.header = Header(self.config["mainUi"]["head"], self)

    def createBody(self):
        self.body = Body(None, self)

    def createFooter(self):
        self.footer = Foot(self.config["mainUi"]["head"], self)

class Header(QtGui.QWidget):
    def __init__(self, j = None, parent = None):
        super(Header, self).__init__(parent)
        self.config = j
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.createCloseButton()
        layout = QtGui.QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        layout.setMargin(0)
        layout.setSpacing(0)
        layout.addWidget(self.closeButton)
        self.setLayout(layout)

    def createCloseButton(self):
        self.closeButton = Button(self.config["closeButton"], self)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(self.config["background-color"][0],\
            self.config["background-color"][1],\
            self.config["background-color"][2],\
            self.config["background-color"][3])
        painter.fillRect(self.rect(), color)

    originPos = None
    isPressed = False
    def mousePressEvent(self, QMouseEvent):
        self.isPressed = True
        self.setCursor(QtCore.Qt.SizeAllCursor)
        self.originPos = QMouseEvent.pos()

    def mouseReleaseEvent(self, QMouseEvent):
        self.isPressed = False
        self.setCursor(QtCore.Qt.ArrowCursor)

    def mouseMoveEvent(self, QMouseEvent):
        if self.isPressed:
            self.parent().move(QMouseEvent.globalPos() - self.originPos)

class Body(QtGui.QWidget):
    """
        对body 进行初始化，嗯，现在采用 label 对每一行进行一个填充？ 使用 textArea 进行填充? 使用其他模型进行填充？
    """
    def __init__(self, j,parent = None):
        super(Body, self).__init__(parent)
        self.config = j
        self.initUi()

    def initUi(self):
        label = QtGui.QLabel()
        label.setText("""\
from PyQt4 import QtGui, QtCore, Qt
import sys
from MainHeader import MainHeader
from MainBody import MainBody
from SideBar import Sidebar
class Constants():
    col = 5
    row = 5
    pageSize = 5
    labelSize = (20,20)
        """)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def paintEvent(self, QPaintEvent):
        pass

class Foot(QtGui.QWidget):
    def __init__(self, j = None, parent = None):
        super(Foot, self).__init__(parent)
        self.config = j
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        #self.createCloseButton()
        layout = QtGui.QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        layout.setMargin(0)
        layout.setSpacing(0)
        #layout.addWidget(self.closeButton)
        self.setLayout(layout)

    def createCloseButton(self):
        self.closeButton = QtGui.QPushButton(self)
        self.closeButton.setStyleSheet("QPushButton{border:none; background-color:rgb(200,200,200)} QPushButton:hover{border:none; background-color:rgb(0,200,200)}")
        self.closeButton.setFixedSize(self.config["closeButton"]["width"], self.config["closeButton"]["height"])

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color = QtGui.QColor(self.config["background-color"][0],\
            self.config["background-color"][1],\
            self.config["background-color"][2],\
            self.config["background-color"][3])
        painter.fillRect(self.rect(), color)

class Menu():
    def __init__(self, j, parent =None):
        super(Menu, self).__init__(parent)

class Button(QtGui.QPushButton):
    def __init__(self, j, parent = None):
        super(Button, self).__init__(parent)
        self.config = j
        self.isPressed = 0x00  #00,10
        self.isEntered = 0x00  #00,01
        self.setFixedSize(self.config["width"], self.config["height"])
        self.initColor()

    def initColor(self):
        self.colorNormal = QtGui.QColor(self.config["background-color"][0],\
            self.config["background-color"][1],\
            self.config["background-color"][2],\
            self.config["background-color"][3])
        self.colorHover = QtGui.QColor(self.config["hover-color"][0],\
            self.config["hover-color"][1],\
            self.config["hover-color"][2],\
            self.config["hover-color"][3])

        self.colorClick = QtGui.QColor(self.config["click-color"][0],\
            self.config["click-color"][1],\
            self.config["click-color"][2],\
            self.config["click-color"][3])

    def paintEvent(self, QPaintEvent):
        status = self.isPressed + self.isEntered
        painter = QtGui.QPainter(self)
        if status == 0:
            painter.fillRect(self.rect(), self.colorNormal)
        elif status == 1:
            painter.fillRect(self.rect(), self.colorHover)
        elif status == 2:
            print("will this kind of case occur?")
        elif status == 3:
            painter.fillRect(self.rect(), self.colorClick)

    def enterEvent(self, *args, **kwargs):
        self.isEntered = 0x01
        self.update()

    def leaveEvent(self, *args, **kwargs):
        self.isEntered = 0x00
        self.update()

    def mousePressEvent(self, *args, **kwargs):
        self.isPressed = 0x02
        self.update()

    def mouseReleaseEvent(self, *args, **kwargs):
        self.isPressed = 0x00
        self.update()

if __name__ == "__main__":
    App = QtGui.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    App.exec()