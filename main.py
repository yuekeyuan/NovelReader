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
        self.createBody()
        self.createHeader()
        self.createFooter()
        self.createMenu()
        self.header.move(self.config["mainUi"]["head"]["x"], self.config["mainUi"]["head"]["y"])
        self.body.move(self.config["mainUi"]["body"]["x"], self.config["mainUi"]["body"]["y"])
        self.footer.move(self.config["mainUi"]["foot"]["x"], self.config["mainUi"]["foot"]["y"])
        self.menu.move(self.config["mainUi"]["menu"]["x"], self.config["mainUi"]["menu"]["y"])
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
            ##head
            self.config["mainUi"]["head"]["x"] = 0
            self.config["mainUi"]["head"]["y"] = 0
            self.config["mainUi"]["head"]["width"] = self.config["mainUi"]["width"]
            self.config["mainUi"]["head"]["height"] = 30
            ####closeButton
            self.config["mainUi"]["head"]["closeButton"]["width"] = 30
            self.config["mainUi"]["head"]["closeButton"]["height"] = 30
            self.config["mainUi"]["head"]["closeButton"]["x"] = self.config["mainUi"]["head"]["width"] - self.config["mainUi"]["head"]["closeButton"]["height"]
            self.config["mainUi"]["head"]["closeButton"]["y"] = 0
            ####maxminButton
            self.config["mainUi"]["head"]["maxminButton"]["width"] = 30
            self.config["mainUi"]["head"]["maxminButton"]["height"] = 30
            self.config["mainUi"]["head"]["maxminButton"]["x"] = self.config["mainUi"]["head"]["width"] - self.config["mainUi"]["head"]["closeButton"]["height"] * 2
            self.config["mainUi"]["head"]["maxminButton"]["y"] = 0
            ####settingButton
            self.config["mainUi"]["head"]["settingButton"]["width"] = 30
            self.config["mainUi"]["head"]["settingButton"]["height"] = 30
            self.config["mainUi"]["head"]["settingButton"]["x"] = self.config["mainUi"]["head"]["width"] - self.config["mainUi"]["head"]["closeButton"]["height"] * 3
            self.config["mainUi"]["head"]["settingButton"]["y"] = 0
            ##foot
            self.config["mainUi"]["foot"]["x"] = 0
            self.config["mainUi"]["foot"]["y"] = self.config["mainUi"]["height"] - self.config["mainUi"]["foot"]["height"]
            self.config["mainUi"]["foot"]["width"] = self.config["mainUi"]["head"]["width"]
            self.config["mainUi"]["foot"]["height"] = self.config["mainUi"]["head"]["height"]
            ##menu
            self.config["mainUi"]["menu"]["x"] = self.config["mainUi"]["head"]["width"] - self.config["mainUi"]["head"]["closeButton"]["height"] * 3
            self.config["mainUi"]["menu"]["y"] = 30
            self.config["mainUi"]["menu"]["width"] = 90
            self.config["mainUi"]["menu"]["height"] = 90
            ##body
            self.config["mainUi"]["body"]["x"] = 0
            self.config["mainUi"]["body"]["y"] = self.config["mainUi"]["head"]["height"]
            self.config["mainUi"]["body"]["width"] = self.config["mainUi"]["width"]
            self.config["mainUi"]["body"]["height"] = self.config["mainUi"]["height"] - self.config["mainUi"]["head"]["height"]
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
        self.body = Body(self.config["mainUi"]["body"], self)
        self.body.setHtml("<h1>hello world</h1><br><h1>this is yuekeyuan</h1>")

    def createFooter(self):
        self.footer = Foot(self.config["mainUi"]["head"], self)

    def createMenu(self):
        self.menu = Menu(self.config["mainUi"]["menu"], self)

class Header(QtGui.QWidget):
    def __init__(self, j = None, parent = None):
        super(Header, self).__init__(parent)
        self.config = j
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        layout = QtGui.QHBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        layout.setMargin(0)
        layout.setSpacing(0)
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

class Body(QtGui.QTextBrowser):
    def __init__(self, j, parent=None):
        """
        看！在这里有一个坑货，我调试了半天，没搞定的 透明度问题，它来一个bug，就啥事都解决了，
        那么问题来了，是Qt 到 pyQt的问题呢？还是原来的Api的问题呢？ (下面的注释保留，以后再看)
        :param j:
        :param parent:
        :return:
        """
        super(Body, self).__init__(parent)
        self.config = j
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        #palette = self.palette()
        #palette.setColor(QtGui.QPalette.All | QPalette.Background, QtGui.QColor(0x00,0xff,0x00,0x00))
        #self.setPalette(palette)
        #self.setAutoFillBackground(True)
        self.setStyleSheet("Body{border:none;background-color:rgb(122,0,0,0.5)}")
        self.setFixedSize(self.config["width"], self.config["height"])

    def initUi(self):
        pass































class Foot(QtGui.QWidget):
    def __init__(self, j = None, parent = None):
        super(Foot, self).__init__(parent)
        self.config = j
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.maxminButton = Button(self.config["maxminButton"], self)
        self.settingButton = Button(self.config["settingButton"], self)
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

class Menu(QtGui.QWidget):
    def __init__(self, j, parent =None):
        super(Menu, self).__init__(parent)
        self.config = j
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.initUi()

    def initUi(self):
        menuClose = Menu.MenuItem(self)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.red)

    class MenuItem(QtGui.QWidget):
        def __init__(self, parent = None):
            super(Menu.MenuItem, self).__init__(parent)
            self.setFixedSize(100,50)
            self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

        def paintEvent(self, QPaintEvent):
            painter = QtGui.QPainter(self)
            painter.fillRect(self.rect(), QtCore.Qt.blue)

class Button(QtGui.QPushButton):
    def __init__(self, j, parent = None):
        super(Button, self).__init__(parent)
        self.config = j
        self.isPressed = 0x00  #00,10
        self.isEntered = 0x00  #00,01
        self.setFixedSize(self.config["width"], self.config["height"])
        self.move(self.config["x"], self.config["y"])
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