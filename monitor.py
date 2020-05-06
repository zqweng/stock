import time
import tushare as ts
import pandas as pd
from threading import Thread
import socket
import pdb
import map_name_code as map_code
import datetime
import os
import json
import numpy as np
from pathlib import Path

#df = myapi.read_csv(r"stock2monitor.csv")
#df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp", period_type="week")

class RealTimeDataTread(Thread):
    def __init__(self, textEdit = None, server_port=0):
        Thread.__init__(self)

        # text box for output
        self.textEdit = textEdit

        #
        self.server_address = ('localhost', server_port)
        self.socket_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
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

        if Path("monitor-vol-result.csv").is_file():
            self.df_result = pd.read_csv("monitor-vol-result.csv")
        else:
            self.df_result = pd.DataFrame(columns=["time", "code", "volume"])
            self.df_result.time = self.df_result.time.astype('datetime64[ns]')
            self.df_result.set_index("time")

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
            sent = self.socket_client.sendto(
            df.to_json(orient='index').encode('utf-8'), self.server_address)
            del df


    def test(self):
        return 1

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
        #self.textEdit.appendPlainText("start index is {} ".format(start))
        #print(df_network)

        for i in range(df_network.shape[0]):
            code = df_network.loc[i].code
            volume = df_network.loc[i].volume
            timestamp = df_network.loc[i].time

            # calculate the volume during this period
            if not pd.isna(self.df_vol.loc[code].lastvol):
                delta_volume = volume - self.df_vol.loc[code].lastvol
            else:
                delta_volume = volume

            #print("code {} delta volume is {}".format(code, delta_volume))

            # if volume is much higher than recent max, print a log
            if delta_volume > (self.df_vol.loc[code].maxvol):
                self.df_result = self.df_result.append(
                    {'time': timestamp, 'code': code, 'volume': volume}, ignore_index=True)
                self.df_result.to_csv("monitor-vol-result.csv")
                #print("code {} has a high volume".format(code))

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

if __name__ == "__main__":
    while True:
        obj = RealTimeDataTread(20001)
        obj.start()
        obj.join()