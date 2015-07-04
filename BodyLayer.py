from PyQt4 import QtCore, QtGui


class TextLayer(QtGui.QTextBrowser):
    def __init__(self, j, parent=None):
        super(TextLayer, self).__init__(parent)
        self.config = j
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
#       palette = self.palette()
#       palette.setColor(QtGui.QPalette.All | QPalette.Background, QtGui.QColor(0x00,0xff,0x00,0x00))
#       self.setPalette(palette)
#       self.setAutoFillBackground(True)
        self.setStyleSheet("TextLayer{border:none;background-color:rgba(0,0,0,0)}")
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.initSettings()
        self.initUi()

    def initSettings(self):
        font = self.font()
        font.setPointSize(20)
        self.setFont(font)

    def initUi(self):
        file = open("README.md", encoding="utf-8")
        a = file.readlines()
        string = ""
        for i in a:
            string = string + i + "\n"
        self.setText(string)


class MaskLayer(QtGui.QWidget):
    def __init__(self, j, parent=None):
        super(MaskLayer, self).__init__(parent)
        self.config = j

        self.entered = 0
        self.pressed = 0

        self.initUi()


    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color   = QtGui.QColor(0, 0, 0, 1)
        painter.fillRect(self.rect(), color)

    def enterEvent(self, QEvent):
        self.entered = 1
        print("entered")

    def leaveEvent(self, QEvent):
        self.entered = 0
        print("left")
    

    def mouseMoveEvent(self, QMouseEvent):
        event = (QtGui.QMouseEvent)(QMouseEvent)
        print(event.pos())
        if self.entered:
            if event.pos().x() > self.rect().x() / 2:
                print("over!")