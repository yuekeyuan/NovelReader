from PyQt4 import QtGui, QtCore
import sys

class MainWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(MainWidget, self).__init__(parent)

    def initUi(self):
        document = QtGui.QTextDocument(self)
        rootDoc  = document.rootFrame()
        textBlock = QtGui.QTextBlock(self)
        textBlockformat = QtGui.QTextBlockFormat(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWidget()
    main.show()
    app.exec()


