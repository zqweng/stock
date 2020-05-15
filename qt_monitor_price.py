
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QVBoxLayout, QListWidget, QPushButton, QGridLayout
import time
import tushare as ts
import pandas as pd
import pdb
import map_name_code as map_code
import datetime
import os
import json
import numpy as np
from pathlib import Path

class MonitorPriceTread(QThread):

    signal = pyqtSignal(str)

    def __init__(self, parent =None):
        super(MonitorPriceTread, self).__init__(parent)

        #
        self.df = pd.read_csv("monitor.csv", converters={'code': lambda x: str(x)})
        self.df = self.df.set_index("code")
        self.range_generator = self.idx_range(self.df.shape[0])

    def idx_range(self, size, start = 0, step = 30):
        # Looping through the file line by line
        n = start
        while True:
            if n + step >= size:
                yield  n, size, 0
                n = 0
            else:
                yield  n, n + step, n + step
                n += step

    def run(self):
        while True:
            # sleep 10 seconds


            now = datetime.datetime.now().time()
            df = self.get_realtime_quote()
            del df
            time.sleep(12)

    def __del__(self):
        self.wait()

    def get_realtime_quote(self):
        # get the code list to be retrieved
        start, end, next_start = next(self.range_generator)

        idx_range = self.df.iloc[start:end].index
        code_list = idx_range.to_list()

        # retrieve the quote of stock list
        df_network = ts.get_realtime_quotes(code_list)

        df_network.replace(to_replace='', inplace=True, value='0')
        df_network = df_network[["name", "open", "pre_close", "price", "time", "code", "volume"]]
        df_network.pre_close = df_network.pre_close.astype("float32")
        df_network.price = df_network.price.astype("float32")
        df_network.volume = df_network.volume.astype("int64")
        df_network.time = df_network.time.astype("string")
        df_network["p_change"] = round((df_network["price"]-df_network["pre_close"]) * 100 /df_network["pre_close"], 3)

        #print(df_network)

        for row in df_network.itertuples():
            monitor_price = self.df.loc[row.code].monitor
            if row.price >= monitor_price:
                self.signal.emit("{},{}, reach target price {}".format(row.code, row.name, monitor_price))
                print("{},{}, reach target price {}".format(row.code, row.name, monitor_price))

        return df_network
