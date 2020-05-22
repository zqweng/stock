
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
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
from qt_monitor_price import *
import webbrowser

class RealTimeDataTread(QThread):

    signal = pyqtSignal(str)

    def __init__(self, parent =None):
        super(RealTimeDataTread, self).__init__(parent)

        #
        self.df = pd.read_csv("stock2monitor-volume.csv", converters={'code': lambda x: str(x)})
        self.df = self.df.set_index("code")
        self.retrieve_count = 0
        self.loop_count = 0
        self.fp = open("monitor.txt","r+")
        self.json = json.load(self.fp)
        self.range_generator = self.idx_range(self.df.shape[0], start=self.json["start"])
        self.time_morning_open = datetime.time(18,30,0)
        self.time_morning_close = datetime.time(20,30,0)
        self.time_afternoon_open = datetime.time(22,0,0)
        self.time_afternoon_close = datetime.time(23,59,0)
        self.time_end_buffer = datetime.timedelta(minutes=20)

        if Path("monitor-vol-data.csv").is_file():
            self.df_vol = pd.read_csv("monitor-vol-data.csv", converters={'code': lambda x: str(x)})
        else:
            self.df_vol = pd.read_csv("monitor-vol.csv", converters={'code': lambda x: str(x)})

        self.df_vol = self.df_vol.set_index("code")
        self.df_vol.curtime = self.df_vol.curtime.astype("string")
        self.df_vol.lasttime = self.df_vol.lasttime.astype("string")
        self.max_ratio = 0.0

        if Path("monitor-vol-result.csv").is_file():
            self.df_result = pd.read_csv("monitor-vol-result.csv")
        else:
            self.df_result = pd.DataFrame(columns=["time", "code", "volume"])
            self.df_result.time = self.df_result.time.astype('datetime64[ns]')
            self.df_result.set_index("time")

        #pdb.set_trace()

    def run(self):
        while True:
            # sleep 10 seconds
            time.sleep(12)

            # get current time, only receive data during trading time
            # there are three timewindws that we dont receive data
            # buffer time is we still need to receive data after morning close since there is a delay


            now = datetime.datetime.now().time()
            #if now <= self.time_morning_open or now >= self.time_afternoon_close:
            #    continue

            #if self.time_morning_close + self.time_end_buffer <= now <= self.time_afternoon_open:
            #    continue
            #pdb.set_trace()
            df = self.get_realtime_quote()
            del df

    def __del__(self):
        self.wait()

    def idx_range(self, size, start = 0, step = 8):
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

        # print current status
        self.retrieve_count += 1
        print("start {}".format(start))
        print(df_network)

        for i in range(df_network.shape[0]):
            code = df_network.loc[i].code
            volume = df_network.loc[i].volume
            timestamp = df_network.loc[i].time
            max_vol = self.df_vol.loc[code].maxvol

            # calculate the volume during this period
            if not pd.isna(self.df_vol.loc[code].lastvol):
                delta_volume = volume - self.df_vol.loc[code].lastvol
            else:
                delta_volume = volume

            #print("code {} delta volume is {}".format(code, delta_volume))

            # if volume is much higher than recent max, print a log
            ratio = delta_volume/max_vol
            print("ration is {}".format(ratio))
            if 1 > ratio > self.max_ratio:
                self.max_ratio = ratio
                self.signal.emit("code {}  has a high volume {}".format(code, ratio))
            if delta_volume > max_vol:
                self.df_result = self.df_result.append(
                    {'time': timestamp, 'code': code, 'volume': volume}, ignore_index=True)
                self.df_result.to_csv("monitor-vol-result.csv")
                self.signal.emit("code {} has a high volume".format(code))

            # save the volume
            self.df_vol.at[code, "curvol"] = volume
            self.df_vol.at[code, "curtime"] = timestamp
            self.df_vol.at[code, "delta"] = delta_volume

        # if this loop is over, move the current volume to last vole
        if next_start == 0:
            self.loop_count += 1
            self.df_vol["lastvol"] = self.df_vol["curvol"]
            self.df_vol["lasttime"] = self.df_vol["curtime"]
            print("new round start, save cur data to last one")


        # save the next index of stock list to be retrieved
        dic = {"start": next_start}
        self.fp.seek(0)
        json.dump(dic, self.fp)
        self.fp.flush()

        self.df_vol.to_csv("monitor-vol-data.csv")

        return df_network


class MyListWidget(QListWidget):
    def __init__(self):
        super(MyListWidget, self).__init__()

    def clicked(self,item):
        str_list = item.text().split(',')
        if (str_list[0][0] == '0'):
            code = 'sz' + str_list[0]
        else:
            code = 'sh' + str_list[0]

        url_str = "http://vip.stock.finance.sina.com.cn/moneyflow/#!ssfx!{}".format(code)
        webbrowser.open(url_str)  # Go to example.com
        #QMessageBox.information(self, "ListWidget", "你选择了: "+item.text())


class MonitorWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Monitor Window"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.thread = MonitorPriceTread()
        self.df = pd.DataFrame(columns=["code", "name"])
        self.df.index = self.df["code"]

        self.listFile = MyListWidget()
        self.btnStart = QPushButton("start")
        self.textEdit = QTextEdit()

        self.listFile.itemClicked.connect(self.listFile.clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.listFile)
        layout.addWidget(self.btnStart)
        layout.addWidget(self.textEdit)

        self.setLayout(layout)

        self.btnStart.clicked.connect(self.slotStart)
        self.thread.signal.connect(self.slotAdd)

    def slotStart(self):
        self.btnStart.setEnabled(False)
        self.thread.start()

    def slotAdd(self,file_inf):
        self.listFile.addItem(file_inf)
        string_list = file_inf.split(',')

        if not string_list[0] in self.df["code"].values:

            print("add {} to dataframe".format(string_list[0]))
            self.df = self.df.append({"code": string_list[0], "name": string_list[1]}, ignore_index=True)
            print(self.df)






if __name__ == "__main__":
        obj = RealTimeDataTread()
        obj.start()
