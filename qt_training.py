from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import random
from mpl_finance import candlestick2_ohlc
from qt_qcompleter import *
from qt_canvas import *

import pdb

class TrainingWindow(QWidget):
    """
        显示K线，并通过按键向前向后移动时间。 并支持更新股票类型。
    """

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
        self.canvas = Canvas(width=12.8, height=9.6, code="002001")

        hlayout = QHBoxLayout()
        button = QPushButton("向前", self)
        button.clicked.connect(self.slot_method_next)

        button2 = QPushButton("向后", self)
        button2.clicked.connect(self.slot_method_prev)

        hlayout.addWidget(button)
        hlayout.addWidget(button2)

        h2layout = QHBoxLayout()

        completer = StockCompleter(self.canvas)
        h2layout.addWidget(completer)

        #
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.canvas)
        vlayout.addLayout(hlayout)
        vlayout.addLayout(h2layout)

        self.setLayout(vlayout)

    def slot_method_next(self):

        self.canvas.plot_next()


    def slot_method_prev(self):

        self.canvas.plot_prev()

