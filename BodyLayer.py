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
        self.horizon = 0   # 左0,右1
        self.vertical = 0  # 上0 下1
        self.leftImage = QtGui.QImage("gallery_button_left.png")
        self.rightImage = QtGui.QImage("gallery_button_right.png")
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.setMouseTracking(True)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color   = QtGui.QColor(0, 0, 0, 1)
        painter.fillRect(self.rect(), color)
        if self.entered and self.horizon:
            painter.drawImage(self.config["width"]-self.rightImage.width(), self.config["height"]/2 - self.rightImage.height() / 2, self.rightImage)
        elif self.entered and self.horizon == 0:
            painter.drawImage(0, self.config["height"]/2 - self.leftImage.height() / 2, self.leftImage)

    def enterEvent(self, QEvent):
        self.entered = 1
        print("entered")
        self.update()

    def leaveEvent(self, QEvent):
        self.entered = 0
        print("left")
        self.update()

    def mouseMoveEvent(self, event):
        if event.pos().x() - self.rect().width()/2 < 0:  #左
            self.horizon = 0
        else:
            self.horizon = 1

        if event.pos().y() - self.rect().height()/2 < 0:  #上
            self.vertical = 0
        else:
            self.vertical = 1

        self.doChange()

    def doChange(self):
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.update()