from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QAction
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pdb
import stock_sample
from qt_ui_monitor import MonitorWindow

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

        self.MyUI()

    def MyUI(self):
        self.canvas = Canvas(self, width=12.8, height=9.6)
        self.canvas.move(0, 0)

        button = QPushButton("向前", self)
        button.move(500, 900)
        button.clicked.connect(self.slot_method_next)

        button2 = QPushButton("向后", self)
        button2.move(700, 900)
        button2.clicked.connect(self.slot_method_prev)

        self.qtMenu()

    def qtMenu(self):
        mainMenu = self.menuBar()
        pyGuiMenu = mainMenu.addMenu('File')

        subItemTable = QAction('New', self)
        subItemTable.setShortcut("Ctrl+N")
        subItemTable.setStatusTip("New Window")

        subItemTable.triggered.connect(self.newWindow)  # +++

        pyGuiMenu.addAction(subItemTable)


    def newWindow(self):  # +++
        self.winTable = MonitorWindow()
        self.winTable.show()

    def slot_method_next(self):
        self.canvas.clear_fig()
        self.canvas.plot_next()
        self.canvas.draw()

    def slot_method_prev(self):
        self.canvas.clear_fig()
        self.canvas.plot_prev()
        self.canvas.draw()


class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=6.4, height=4.8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axe = self.fig.subplots()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        #
        self.set_axe()

        #
        self.sample = stock_sample.StockSample(self.axe)

    def plot_next(self):
        self.sample.plot_next(self.axe)

    def plot_prev(self):
        self.sample.plot_prev(self.axe)

    def clear_fig(self):
        self.fig.clf()
        self.set_axe()

    def set_axe(self):
        gs = self.fig.add_gridspec(5, 1)
        self.axe = []
        self.axe.append(self.fig.add_subplot(gs[0:-1, :]))
        self.axe.append(self.fig.add_subplot(gs[-1:, :]))



app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()