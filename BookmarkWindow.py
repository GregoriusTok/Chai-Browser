import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import pyperclip

class BookmarkWindow(QWidget):
    def __init__(self, currentUrl):
        super().__init__()

        self.currentUrl = currentUrl

        self.setWindowTitle("Bookmarks")

        self.top = 200
        self.left = 1500
        self.width = 300
        self.height = 600
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.bookmarkListTemp = []
        with open("Bookmarks.txt", "r") as file:
            self.bookmarkListTemp = file.readlines()

        self.bookmarkList = []
        for i in self.bookmarkListTemp:
            self.bookmarkList.append(i.replace("\n", ""))

        self.lay = QGridLayout()

        self.list = QListWidget()
        self.list.addItems(self.bookmarkList)
        self.list.itemActivated.connect(self.activation)

        self.newBookB = QPushButton(text="New Bookmark")
        self.newBookB.clicked.connect(self.newBook)

        self.url = ""

        self.lay.addWidget(self.newBookB)
        self.lay.addWidget(self.list)
        self.setLayout(self.lay)

    def activation(self, item):
        self.url = item.text()
        pyperclip.copy(self.url)

        self.notification("URL Copied to Clipboard")

        self.close()

    def newBook(self):
        if self.currentUrl not in self.bookmarkList:
            with open("Bookmarks.txt", "a") as file:
                file.write(self.currentUrl + "\n")
            self.updateList()
            self.close()
        else:
            self.notification("Already Bookmarked")

    def updateList(self):
        self.bookmarkListTemp = []
        with open("Bookmarks.txt", "r") as file:
            self.bookmarkListTemp = file.readlines()

        self.bookmarkList = []
        for i in self.bookmarkListTemp:
            self.bookmarkList.append(i.replace("\n", ""))
        
        self.list.clear()
        self.list.addItems(self.bookmarkList)
        
        self.list.update()
    
    def notification(self, text):
        self.Notif = QWidget()
        self.Notif.setGeometry(self.left, self.top, self.width, 50)
        self.Notif.setWindowTitle("Notification")
        self.NotifLay = QGridLayout()
        self.NotifLay.addWidget(QLabel(text))
        self.Notif.setLayout(self.NotifLay)
        self.Notif.show()

if __name__ == "__Main__":
    app = QApplication([])
    b =BookmarkWindow()
    b.show()
    app.exec()