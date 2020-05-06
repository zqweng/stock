from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pdb
import qt_training
from qt_monitor import MonitorWindow
from qt_training import TrainingWindow
from qt_favorite import FavoriteWindow

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Matplotlib Embeding In PyQt5"
        top = 0
        left = 0
        width = 1200
        height = 1000

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        self.qtMenu()

    def qtMenu(self):
        mainMenu = self.menuBar()
        pyGuiMenu = mainMenu.addMenu('工具')

        subItemTable = QAction('Monitor', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.setStatusTip("New Window")
        subItemTable.triggered.connect(self.startMonitor)  # +++
        pyGuiMenu.addAction(subItemTable)

        subItemTable = QAction('Training', self)
        subItemTable.setShortcut("Ctrl+S")
        subItemTable.setStatusTip("New Window")
        subItemTable.triggered.connect(self.startTraining)  # +++
        pyGuiMenu.addAction(subItemTable)

        subItemTable = QAction('MyFavorite', self)
        subItemTable.setShortcut("Ctrl+D")
        subItemTable.setStatusTip("My Favorite")
        subItemTable.triggered.connect(self.startFavorite)  # +++
        pyGuiMenu.addAction(subItemTable)


    def startMonitor(self):  # +++
        self.winTable = MonitorWindow()
        self.winTable.show()

    def startTraining(self):  # +++
        self.trainingWindow = TrainingWindow()
        self.trainingWindow.show()

    def startFavorite(self):  # +++
        self.favoriteWindow = FavoriteWindow()
        self.favoriteWindow.show()


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()