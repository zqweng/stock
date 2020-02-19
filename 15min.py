import stock_library2 as lib2
import driver5 as dr5
import pandas as pd
import pdb
import get_realtime_data as rt
import api as myapi

"""
df = myapi.read_csv(r"result\ma20-final-2020-02-18.csv")
df = df[df["p2"] < 0.8]
df = df[df["p2"] >= 0.6]
df = df[df["p_change"] >=6]
df.to_csv(r"result\ma20-2020-02-18-6p.csv")

"""

def print_15min_vol_num(stock_list):
    for code in stock_list:
        df = pd.read_csv("C:\\Users\\johnny\\stockdata-bao\\15\\{}.csv".format(code), nrows=16)
        df["p_change"] = round((df["close"] - df["open"]) * 100 / df["open"], 3)
        df1 = df[df["p_change"] > 1]
        df2 = df[df["p_change"] < -1]
        print("code {} num above %1 is {}, less than%-1 is {} ".format(code, len(df1.index), len(df2.index)))
        pdb.set_trace()

print_15min_vol_num(["600661"])