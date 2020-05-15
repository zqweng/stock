from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import random
from mpl_finance import candlestick2_ohlc
from qt_qcompleter import *

import pdb

class TrainingWindow(QWidget):
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
        self.canvas.clear_fig()
        self.canvas.plot_next()
        self.canvas.draw()

    def slot_method_prev(self):
        self.canvas.clear_fig()
        self.canvas.plot_prev()
        self.canvas.draw()




class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=6.4, height=4.8, dpi=100, code=""):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        #
        self.set_axe()

        #
        self.sample = StockSample(self.axe, code)

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

    def set_new_code(self, code):
        self.clear_fig()
        del self.sample
        self.sample = StockSample(self.axe, code)
        self.draw()

class StockSample():
    def __init__(self, ax, code=""):

        self.start_plot(ax, code)

    def start_plot(self, ax, code = ""):
        self.df = pd.read_csv("/home/johnny/stockdata-bao/day/{}.csv".format(code), nrows=300)
        self.max_record = self.df.shape[0]
        self.df = self.df.iloc[::-1]
        #self.df = self.df.reset_index()
        self.counter = 130
        self.display_num = 150

        df_slice = self.df[self.counter: self.counter + self.display_num]

        df_slice = df_slice.reset_index()

        self.plot(ax, df_slice)

    def plot_next(self,ax):

        if self.counter + self.display_num < self.max_record:
            self.counter += 1

        df_slice = self.df[self.counter: self.display_num + self.counter]
        df_slice = df_slice.reset_index()

        self.plot(ax,df_slice)

    def plot_prev(self,ax):

        self.counter -= 1 if self.counter > 0 else 0

        df_slice = self.df[self.counter: self.display_num + self.counter]
        df_slice = df_slice.reset_index()

        self.plot(ax,df_slice)

    def plot(self, ax, df_slice):

        candlestick2_ohlc(ax[0], df_slice['open'], df_slice['high'], df_slice['low'], df_slice['close'],
                          width=0.6, colorup='r', colordown='k',)
        ax[0].plot(df_slice["ma5"], "k", label="ma5", linewidth=0.5)
        ax[0].plot(df_slice["ma10"], "y", label="ma10", linewidth=0.5)
        ax[0].plot(df_slice["ma20"], "r", label="ma20", linewidth=0.5)
        ax[0].plot(df_slice["upper"], "b--", label="upper", linewidth=0.5)
        ax[0].plot(df_slice["lower"], "b--", label="upper", linewidth=0.5)
        text = df_slice.tail(1).p_change.values[0]
        ax[0].set_title("price change {}".format(str(text)))

        color = ""
        for x in df_slice['p_change']:
            if x >= 0:
                color += 'r'
            else:
                color += 'k'

        ax[1].bar(df_slice.index, df_slice["volume"], color = color)





