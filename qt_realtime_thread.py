
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

class QRealTimeTread(QThread):

    signal = pyqtSignal(str)

    def __init__(self, parent =None):
        super(QRealTimeTread, self).__init__(parent)

        #
        self.df = pd.read_csv("mystocklist_detail.csv", converters={'code': lambda x: str(x)})
        self.df = self.df.set_index("code")
        self.range_generator = self.idx_range(self.df.shape[0])


    def run(self):
        duration = 0
        while True:
            # sleep 10 seconds

            self.get_realtime_quote()
            time.sleep(12)
            duration += 12
            print("thread time {}".format(duration))

    def __del__(self):
        self.wait()

    def idx_range(self, size, start = 0, step = 50):
        # Looping through the file line by line
        n = start
        while True:
            if n + step >= size:
                yield  n, size, 0
                n = 0
            else:
                yield  n, n + step, n + step
                n += step


    def get_realtime_quote(self):
        # get the code list to be retrieved
        step = 25
        df = pd.DataFrame()
        for i in range(0, len(self.df.index), step):
            idx_range = self.df.iloc[i: i + step].index
            code_list = idx_range.to_list()

            # retrieve the quote of stock list
            df_network = ts.get_realtime_quotes(code_list)
            df_network.replace(to_replace='', inplace=True, value='0')
            df_network = df_network[["name", "open", "pre_close", "price", "time", "code", "volume"]]
            df_network.open = df_network.open.astype("float").round(2)
            df_network.pre_close = df_network.pre_close.astype("float").round(2)
            df_network.price = df_network.price.astype("float").round(2)
            df_network.volume = df_network.volume.astype("int64")
            df_network.time = df_network.time.astype("string")
            df_network["p_change"] = round((df_network["price"]-df_network["pre_close"]) * 100 /df_network["pre_close"], 3)
            df = pd.concat([df, df_network])

        df = df.reset_index()
        df = df.drop(columns="index")
        string = df.to_json(orient='index')
        self.signal.emit(string)
        #print(df_network)
        del df_network


if __name__ == "__main__":
        obj = RealTimeDataTread()
        obj.start()
