from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout,QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import random
from mpl_finance import candlestick2_ohlc
from qt_qcompleter import *
from qt_search_cmd import update_stock_list, download_30min
import threading

import pdb

class ToolWindow(QWidget):
    def __init__(self):
        super().__init__()

        title = "tool window"
        top = 0
        left = 0
        width = 1200
        height = 1000

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        self.MyUI()

    def MyUI(self):

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        button = QPushButton("开始", self)
        button.clicked.connect(self.on_start)

        self.cbStockList = QCheckBox("更新股票列表文件")
        self.cbDownload30Min = QCheckBox("下载30分钟线")
        self.textbox = QTextEdit()


        vlayout.addWidget(self.cbDownload30Min)
        vlayout.addWidget(self.cbStockList)
        vlayout.addWidget(self.textbox)
        vlayout.addWidget(button)

        self.setLayout(vlayout)

    def on_start(self):
        if self.cbStockList.isChecked():
            x = threading.Thread(target=update_stock_list)
            x.start()

        if self.cbDownload30Min.isChecked():
            x = threading.Thread(target=download_30min)
            x.start()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=ToolWindow()
    demo.show()
    sys.exit(app.exec_())


