from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pdb
import stock_sample
from qt_ui_monitor import MonitorWindow
from stock_sample import TrainingWindow

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
        pyGuiMenu = mainMenu.addMenu('File')

        subItemTable = QAction('Monitor', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.setStatusTip("New Window")

        subItemTable.triggered.connect(self.newWindow)  # +++

        pyGuiMenu.addAction(subItemTable)

        subItemTable = QAction('Training', self)
        subItemTable.setShortcut("Ctrl+S")
        subItemTable.setStatusTip("New Window")

        subItemTable.triggered.connect(self.newTrainingWindow)  # +++

        pyGuiMenu.addAction(subItemTable)

    def newWindow(self):  # +++
        self.winTable = MonitorWindow()
        self.winTable.show()

    def newTrainingWindow(self):  # +++
        self.trainingWindow = TrainingWindow()
        self.trainingWindow.show()

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()