from PyQt4 import QtGui, QtCore

class Document():
    def __init__(self):
        self.articlePath = None
        self.articleContent = None
        self.articleFile = None

        self.totalPageIndex = 0
        self.currentPageIndex = 0

        self.currentCharacterCount = None
        self.totalCharacterCount = None

        self.previousPageContent = None
        self.currentPageContent = None
        self.nextPageContent = None

    def setArticlePath(self, path):
        self.articlePath = path
        self.articleFile = open("")

    def getTotalPageIndex(self):
        return self.totalPageIndex

    def getCurrentPageCount(self):
        return self.currentPageIndex, self.currentPageContent

    def getNextPageContent(self):
        if self.currentPageIndex == self.totalPageIndex:
            return "-1", self.currentPageContent
        self.previousPageContent = self.currentPageContent
        self.currentPageContent = self.nextPageContent
        self.nextPageContent = self.generateNexPage()
        self.currentPageIndex = self.currentPageIndex + 1

        return self.currentPageIndex, self.currentPageContent

    def getPreviousPageContent(self):
        if self.currentPageIndex == 0:
            return "-2", self.currentPageContent
        self.nextPageContent = self.currentPageContent
        self.currentPageContent = self.previousPageContent
        self.previousPageContent = self.generatePreviousPage()
        self.currentPageIndex = self.currentPageIndex - 1

        return self.currentPageIndex, self.currentPageContent

    def close(self):
        pass

    def __dividePage(self):
        pass

    def generateNexPage(self):
        pass

    def generatePreviousPage(self):
        pass


