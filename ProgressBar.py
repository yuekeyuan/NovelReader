from PyQt4 import QtCore, QtGui

class ProgressBar(QtGui.QWidget):
    """
    这一个类和parent的widget紧密相关，所以我们必须保存parent的值
    """
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)
        self.parent = parent

    def initUi(self):
        self.resize(2,2)
        self.move(self.parent.rect().width() - 5, 0)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0,0,0,0))
        painter.fillRect(QtCore.QRectF(1, 0, self.width(), self.height()), QtCore.Qt.red)



