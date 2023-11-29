import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Title
        self.title = "Chai"
        self.setWindowTitle(self.title)

        #Dimensions/position
        self.top = 200
        self.left = 200
        self.width = 1200
        self.height = 600
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Google
        self.defaultUrl = "https://www.google.com/"

        #ToolBar
        self.initToolBar()
        self.addToolBar(self.bar)
        #TabBar
        self.initTabBar()
        
        self.show()
    
    def initToolBar(self):
        #ToolBar
        self.bar = QToolBar()
        #SearchBar
        self.search = QLineEdit()
        self.search.returnPressed.connect(self.updateUrl)
        #Search Button
        self.searchB= QPushButton("Search")
        self.searchB.clicked.connect(self.updateUrl)
        #Add Tab
        self.addTabB = QPushButton("+")
        self.addTabB.clicked.connect(self.addTab)
        self.addTabB.setFixedWidth(30)
        
        #Previous
        self.backB = QPushButton("<")
        self.backB.clicked.connect(self.back)
        self.backB.setFixedWidth(30)
        #Forwards
        self.forwB = QPushButton(">")
        self.forwB.clicked.connect(self.forward)
        self.forwB.setFixedWidth(30)
        #Reload
        self.relB = QPushButton("⟳")
        self.relB.clicked.connect(self.reload)
        self.relB.setFixedWidth(30)
        
        self.bar.addWidget(self.backB)
        self.bar.addWidget(self.forwB)
        self.bar.addWidget(self.relB)
        self.bar.addWidget(self.addTabB)
        self.bar.addWidget(self.search)
        self.bar.addWidget(self.searchB)
    
    def initTabBar(self):
        #TabBar
        self.tabs = QTabWidget()
        self.addTab()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.tabs)
    
    def addTab(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl(self.defaultUrl))
        self.tabs.addTab(browser, 'New Tab')
        self.tabs.setCurrentWidget(browser)

        browser.titleChanged.connect(lambda title, browser=browser: self.tabs.setTabText(self.tabs.indexOf(browser), title))
        browser.urlChanged.connect(self.urlChange)

    def closeTab(self, index):
        if self.tabs.count() < 2:
            self.close()
        else:
            self.tabs.removeTab(index)
    
    def updateUrl(self):
        self.url = self.search.text()
        if "." not in self.url:
            self.url = "https://www.google.com/search?q="+self.url
        elif "https://" not in self.url:
            self.url = "https://" + self.url
        
        self.tabs.currentWidget().setUrl(QUrl(self.url))

    def urlChange(self, url):
        self.search.setText(url.toString())

        if url.toString() != self.defaultUrl:
            with open("History.txt", "a") as file:
                file.write(url.toString() + "\n")
    
    def reload(self):
        self.tabs.currentWidget().reload()

    def back(self):
        self.tabs.currentWidget().back()

    def forward(self):
        self.tabs.currentWidget().forward()

if __name__ == "__main__":
    app = QApplication([])
    mainWindow=mainWindow()
    app.exec()