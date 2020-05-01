import time
import tushare as ts
import pandas as pd
from threading import Thread
import socket
import pdb
import map_name_code as map_code

class RealTimeDataTread(Thread):
    def __init__(self, server_port=0, stock_list=""):
        Thread.__init__(self)
        self.server_address = ('localhost', server_port)
        self.socket_client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.stock_list = stock_list

    def run(self):
        while True:
            df = self.get_realtime_quote()
            sent = self.socket_client.sendto(
                df.to_json(orient='index').encode('utf-8'), self.server_address)
            time.sleep(10)

    def get_realtime_quote(self):
        df = ts.get_realtime_quotes(self.stock_list)
        df.replace(to_replace='', inplace=True, value='0')
        df = df[["name", "open", "pre_close", "price", "time", "code"]]
        df.pre_close = df.pre_close.astype("float32")
        df.price = df.price.astype("float32")
        df["p_change"] = round((df["price"]-df["pre_close"]) * 100 /df["pre_close"], 3)
        print(df)
        return df

if __name__ == "__main__":
    ex_li = ["002328", "002258", "603839", "002002", "603920", "002688", "002373", "002237", "002829", "600267", "002756",
             "002803", "603583", "002383", "002180", "002527"]
    name_list = ['高德红外', '捷昌驱动', '大立科技', '江化微', '能科股份',
                 '奥翔药业', '圣达生物',  '百傲化学',  '上实发展',
                 '北大荒', '维维股份','克明面业', '粤桂股份', '丰乐种业',
                 '华资实业', '*ST 南糖', '金财互联', '广电运通', '格尔软件',
                 '众应互联', '冠农股份'
                 ]
    code_list = map_code.getCodeList(name_list)
    code_list.extend(["000001", "399001", "399006"])
    print(code_list)
    while True:
        obj = RealTimeDataTread(20001, code_list)
        obj.start()
        obj.join()