import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from HistoryWindow import HistoryWindow
from BookmarkWindow import BookmarkWindow

class MainWindow(QMainWindow):
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

        self.setStyleSheet("background-color: violet; border: 2px solid black")

        #Google
        self.defaultUrl = "https://www.google.com/"
        self.currentUrl = self.defaultUrl

        #ToolBar
        self.initToolBar()
        self.addToolBar(self.bar)
        #TabBar
        self.initTabBar()
        
        self.show()

    def initToolBar(self):
        #ToolBar
        self.bar = QToolBar()
        self.bar.setStyleSheet("background-color: purple; color: white; border: 0px; border-left: 5px solid purple; border-right: 5px solid purple;")
        #SearchBar
        self.search = QLineEdit()
        self.search.setStyleSheet("border: 2px solid indigo")
        self.search.returnPressed.connect(self.updateUrl)
        #Search Button
        self.searchB= QPushButton("Search")
        self.searchB.setStyleSheet("border-right: 1px solid violet; border-bottom: 1px solid violet")
        self.searchB.clicked.connect(self.updateUrl)
        #Add Tab
        self.addTabB = QPushButton("+")
        self.addTabB.setStyleSheet("border-right: 1px solid violet; border-bottom: 1px solid violet")
        self.addTabB.clicked.connect(self.addTab)
        self.addTabB.setFixedWidth(30)
        
        #Previous
        self.backB = QPushButton("<")
        self.backB.clicked.connect(self.back)
        self.backB.setStyleSheet("border-right: 1px solid violet; border-bottom: 1px solid violet")
        self.backB.setFixedWidth(30)
        self.backS = QShortcut(QKeySequence("Ctrl+Shift+J"), self).activated.connect(self.back)
        #Forwards
        self.forwB = QPushButton(">")
        self.forwB.clicked.connect(self.forward)
        self.forwB.setStyleSheet("border-right: 1px solid violet; border-bottom: 1px solid violet")
        self.forwB.setFixedWidth(30)
        self.forwS = QShortcut(QKeySequence("Ctrl+Shift+L"), self).activated.connect(self.forward)
        #Reload
        self.relB = QPushButton("⟳")
        self.relB.clicked.connect(self.reload)
        self.relB.setStyleSheet("border-right: 1px solid violet; border-bottom: 1px solid violet")
        self.relB.setFixedWidth(30)
        self.relS = QShortcut(QKeySequence("Ctrl+R"), self).activated.connect(self.reload)
        #History
        self.hisB = QPushButton("H")
        self.hisB.clicked.connect(self.historyWindow)
        self.hisB.setStyleSheet("border-right: 1px solid violet; border-bottom: 1px solid violet")
        self.hisB.setFixedWidth(30)
        self.hisS = QShortcut(QKeySequence("Ctrl+H"), self).activated.connect(self.historyWindow)
        #Bookmarks
        self.bookB = QPushButton("B")
        self.bookB.clicked.connect(self.bookmarkWindow)
        self.bookB.setStyleSheet("border-right: 1px solid violet; border-bottom: 1px solid violet")
        self.bookB.setFixedWidth(30)
        self.bookS = QShortcut(QKeySequence("Ctrl+B"), self).activated.connect(self.bookmarkWindow)
    
        self.bar.addWidget(self.backB)
        self.bar.addWidget(self.forwB)
        self.bar.addWidget(self.relB)
        self.bar.addWidget(self.addTabB)
        self.bar.addWidget(self.search)
        self.bar.addWidget(self.searchB)
        self.bar.addWidget(self.hisB)
        self.bar.addWidget(self.bookB)
        
    def initTabBar(self):
        #TabBar
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {border-left: 3px solid black; border-right: 3px solid black; border-bottom: 3px solid black;}  
            QTabWidget::tab-bar {left: 0px;} 
            QTabBar::tab:selected {color: white; background-color: green; border: 5px solid green;} 
            QTabBar::tab:!selected {color: white; background-color: black; border: 5px solid black;}
        """)
        self.addTab()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        self.setCentralWidget(self.tabs)

    def addTab(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl(self.defaultUrl))
        browser.setZoomFactor(1.25)
        self.tabs.addTab(browser, 'New Tab')
        self.tabs.setCurrentWidget(browser)

        browser.titleChanged.connect(lambda title, browser=browser: self.tabs.setTabText(self.tabs.indexOf(browser), title))
        browser.urlChanged.connect(self.urlChange)

    def closeTab(self, index):
        browserW = self.tabs.widget(index)
        browserW.page().runJavaScript("document.getElementsByTagName('video')[0].pause();")

        if self.tabs.count() < 2:
            self.close()
        else:
            self.tabs.removeTab(index)

    def updateUrl(self):
        self.url = self.search.text()
        if self.url.upper() in ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE', 'INDIGO', 'VIOLET']:
            self.setStyleSheet("background-color: " + self.url.lower())
        if "." not in self.url:
            self.url = "https://www.google.com/search?q="+self.url
        elif "https://" not in self.url:
            self.url = "https://" + self.url
        
        self.tabs.currentWidget().setUrl(QUrl(self.url))

    def urlChange(self, url):
        self.search.setText(url.toString())
        self.currentUrl = url.toString()

        if url.toString() != self.defaultUrl:
            with open("History.txt", "a") as file:
                file.write(url.toString() + "\n")
    
    def reload(self):
        self.tabs.currentWidget().reload()

    def back(self):
        self.tabs.currentWidget().back()

    def forward(self):
        self.tabs.currentWidget().forward()
    
    def historyWindow(self):
        self.historyWindowV = HistoryWindow()
        self.historyWindowV.show()

    def bookmarkWindow(self):
        self.bookmarkWindowV = BookmarkWindow(self.currentUrl)
        self.bookmarkWindowV.show()
    
    def closeEvent(self, event):
        QApplication.closeAllWindows()
        event.accept()

if __name__ == "__main__":
    app = QApplication([])
    MainWindow=MainWindow()
    app.exec()