import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
import pyperclip

class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("History")

        self.top = 200
        self.left = 1500
        self.width = 300
        self.height = 600
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.historyListTemp = []
        with open("History.txt", "r") as file:
            self.historyListTemp = file.readlines()

        self.historyList = []
        for i in self.historyListTemp:
            self.historyList.insert(0, i.replace("\n", ""))

        self.lay = QGridLayout()

        self.list = QListWidget()
        self.list.addItems(self.historyList)
        self.lay.addWidget(self.list)
        self.list.itemActivated.connect(self.activation)

        self.url = ""

        self.setLayout(self.lay)

    def activation(self, item):
        self.pastUrl = item.text()
        pyperclip.copy(self.pastUrl)

        self.copyNotif = QWidget()
        self.copyNotif.setGeometry(self.left, self.top, self.width, 50)
        self.copyNotif.setWindowTitle("Notification")
        self.copyNotifLay = QGridLayout()
        self.copyNotifLay.addWidget(QLabel("URL Copied to Clipboard"))
        self.copyNotif.setLayout(self.copyNotifLay)
        self.copyNotif.show()

        self.close()

if __name__ == "__Main__":
    app = QApplication([])
    h = HistoryWindow()
    h.show()
    app.exec()