from PyQt4 import QtCore, QtGui
from ProgressBar import ProgressBar
import threading

class FileReaderInterface():
    def nextPage(self):
        pass
    def previousPage(self):
        pass
    def leftSlide(self):
        pass
    def rightSlide(self):
        pass

class TextLayer(QtGui.QTextBrowser, FileReaderInterface):
    def __init__(self, j, parent=None):
        super(TextLayer, self).__init__(parent)
        self.config = j
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.initSettings()
        self.initUi("README.md")

    def initSettings(self):
        self.setContentsMargins(0, 0, 0, 0)
        font = self.font()
        font.setPointSize(14)
        self.setFont(font)

        palette = self.palette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtCore.Qt.NoBrush))
        self.setPalette(palette)

        self.setFixedSize(self.config["width"], self.config["height"])
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("TextLayer{background:rgb(0,0,0); border:none; padding:0 0;}")

    def initUi(self, fileName):
        file = open(fileName, encoding="utf-8")
        print(self.parent().parent().setFileName(fileName))
        a = file.readlines()
        string = ""
        for i in a:
            string = string + i
        self.setText(string)

    def openFile(self, fileName):
        self.initUi(fileName)

    line = 4
    def nextPage(self):
        if self.line >= self.verticalScrollBar().maximum():
            self.parent().info.setInfo("this is the end of file", 2)
            return
        font = self.font()
        matrix = QtGui.QFontMetrics(font)
        print("max: ", self.verticalScrollBar().maximum(), "min,", self.verticalScrollBar().minimum())
        height = self.rect().height() - self.rect().height() % matrix.lineSpacing()
        self.line = self.line + height

        self.verticalScrollBar().setValue(self.line)
        print("line space", matrix.lineSpacing())
        print(self.line)

    def previousPage(self):
        if self.line <= 0:
            self.parent().info.setInfo("this is the head of file", 2)
            return
        font = self.font()
        matrix = QtGui.QFontMetrics(font)
        height = self.rect().height() - self.rect().height() % matrix.lineSpacing()
        self.line = self.line - height
        self.verticalScrollBar().setValue(self.line)
        print(self.line)

    def leftSlide(self):
        pass

    def rightSlide(self):
        pass

    def getCurrentValue(self):
        return self.verticalScrollBar().value()

class MaskLayer(QtGui.QWidget):
    def __init__(self, j, parent=None):
        super(MaskLayer, self).__init__(parent)
        self.config = j
        self.isDrag = False
        self.entered = 0
        self.pressed = 0
        self.horizon = 0   # 左0,右1
        self.vertical = 0  # 上0 下1
        self.leftImage = QtGui.QImage("gallery_button_left.png")
        self.rightImage = QtGui.QImage("gallery_button_right.png")

        self.originY = 0
        self.MoveY = 0
        self.pageY = 0

        #self.cur_move = QtGui.QCursor(QtGui.QPixmap("cur_move.png"))
        #self.cur_static = QtGui.QCursor(QtGui.QPixmap("cur_static.png"))
        #self.setMouseTracking(True)
        #self.setCursor(self.cur_static)
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])
        self.progressBar = ProgressBar(self)
        self.setMouseTracking(True)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        color   = QtGui.QColor(0, 0, 0, 1)
        painter.fillRect(self.rect(), color)

    def enterEvent(self, QEvent):
        self.entered = 1
        print("entered")
        self.update()

    def leaveEvent(self, QEvent):
        self.entered = 0
        print("left")
        self.update()

    def mousePressEvent(self, QMouseEvent):
        self.isDrag = True
        self.pageY = self.parent().body.getCurrentValue()
        print(self.pageY)
        self.originY = QMouseEvent.pos().y()

    def mouseReleaseEvent(self, QMouseEvent):
        self.isDrag = False

    def mouseMoveEvent(self, event):

        if self.isDrag:
            self.moveY = event.pos().y() - self.originY + self.pageY
            print(self.originY)
            self.parent().body.verticalScrollBar().setValue(self.moveY)

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

class InfoLayer(QtGui.QWidget):

    INFO_LONG_SHOW   = 3000
    INFO_MIDDLE_SHOW = 1500
    INFO_SHORT_SHOW  = 1000

    def __init__(self, j, parent=None):
        super(InfoLayer, self).__init__(parent)
        self.config = j

        self.timer = None
        self.alpha = 0
        self.state = 0
        self.infoString = ""
        self.isShow = False
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.config["width"], self.config["height"])

    def paintEvent(self, QPaintEvent):
        if self.isShow:
            painter = QtGui.QPainter(self)
            color   = QtGui.QColor(0, 0, 0, 0)
            painter.fillRect(self.rect(), color)

            font = self.font()
            metrix = QtGui.QFontMetrics(font)
            h = metrix.height()
            w = metrix.width(self.infoString)
            x = (self.config["width"] - w) /2
            y = (self.config["height"]*3/2 - h)/2
            path = QtGui.QPainterPath()
            path.addRoundedRect(x, y, w + 30, h + 10 , 3, 3)
            painter.fillPath(path, QtGui.QBrush(QtGui.QColor(212,200,200,self.alpha)))
            painter.setPen(QtGui.QColor(0, 0, 0, self.alpha))
            painter.drawText(QtCore.QPointF(x + 15, y + 15), self.infoString)

    def setInfo(self, string, time):
        self.infoString = string
        self.isShow = True
        if self.timer != None:
            self.timer.cancel()
        self.showInfo(0.01,time,0.01)

    def showInfo(self, uptime, equaltime, downTime):
        print(self.alpha)
        if self.alpha >= 230 and self.state == 0:
            print("this happen ....................................")
            self.state = 1
            self.timer = threading.Timer(equaltime, self.showInfo, [uptime, equaltime, downTime])
            self.timer.start()
            return

        if self.alpha < 255 and self.state == 0:
            self.alpha = self.alpha + 10
            self.update()
            self.timer = threading.Timer(uptime, self.showInfo, [uptime, equaltime, downTime])
            self.timer.start()
            return

        if self.alpha > 0 and self.state == 1:
            self.alpha = self.alpha - 10
            self.update()
            self.timer = threading.Timer(downTime, self.showInfo, [uptime, equaltime, downTime])
            self.timer.start()
        else:
            self.alpha = 0
            self.state = 0
            self.isShow = False
            self.timer.cancel()
            self.timer = None
