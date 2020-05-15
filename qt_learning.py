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
from qt_tool_window import *
from qt_tab import *
from qt_sell_diagnose import *
from qt_table import *

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
        pyGuiMenu = mainMenu.addMenu('管理')

        subItemTable = QAction('Monitor', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.setStatusTip("New Window")
        subItemTable.triggered.connect(self.on_start_monitor)  # +++
        pyGuiMenu.addAction(subItemTable)

        subItemTable = QAction('Training', self)
        subItemTable.setShortcut("Ctrl+S")
        subItemTable.setStatusTip("New Window")
        subItemTable.triggered.connect(self.on_start_training)  # +++
        pyGuiMenu.addAction(subItemTable)

        subItemTable = QAction('MyFavorite', self)
        subItemTable.setShortcut("Ctrl+D")
        subItemTable.setStatusTip("My Favorite")
        subItemTable.triggered.connect(self.on_start_favorite)  # +++
        pyGuiMenu.addAction(subItemTable)

        subItemTable = QAction('工具', self)
        subItemTable.setShortcut("Ctrl+G")
        subItemTable.setStatusTip("工具")
        subItemTable.triggered.connect(self.on_start_tool)  # +++
        pyGuiMenu.addAction(subItemTable)

        pyGuiMenu = mainMenu.addMenu('诊断')

        subItemTable = QAction('卖股', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.setStatusTip("卖股")
        subItemTable.triggered.connect(self.on_start_diagnose_sell)  # +++
        pyGuiMenu.addAction(subItemTable)

        pyGuiMenu = mainMenu.addMenu('选股')

        subItemTable = QAction('选股', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.setStatusTip("选股")
        subItemTable.triggered.connect(self.on_start_search)  # +++
        pyGuiMenu.addAction(subItemTable)

        subItemTable = QAction('财表', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.setStatusTip("财表")
        subItemTable.triggered.connect(self.on_start_finance)  # +++
        pyGuiMenu.addAction(subItemTable)

    def on_start_finance(self):
        self.infoWindow = InfoTable()
        self.infoWindow.show()

    def on_start_search(self):
        self.searchWindow = SearchWindow()
        self.searchWindow.show()

    def on_start_tool(self):
        self.toolWindow = ToolWindow()
        self.toolWindow.show()

    def on_start_monitor(self):  # +++
        self.winTable = MonitorWindow()
        self.winTable.show()

    def on_start_training(self):  # +++
        self.trainingWindow = TrainingWindow()
        self.trainingWindow.show()

    def on_start_favorite(self):  # +++
        self.favoriteWindow = FavoriteWindow()
        self.favoriteWindow.show()

    def on_start_diagnose_sell(self):
        self.sellDiagnoseWindow = SellDiagnoseWindow()
        self.sellDiagnoseWindow.show()

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()