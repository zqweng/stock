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

#df1 = dr5.get_a_across_b(period_of_days=16, cross_type="vol-pct-count", period_type="15")
#pdb.set_trace()
def print_15min_vol_num(stock_list):
    for code in stock_list:
        df = pd.read_csv("C:\\Users\\johnny\\stockdata-bao\\15\\{}.csv".format(code), nrows=16)
        df["p_change"] = round((df["close"] - df["open"]) * 100 / df["open"], 3)
        df1 = df[df["p_change"] > 1]
        df2 = df[df["p_change"] < -1]
        print("code {} num above %1 is {}, less than%-1 is {} ".format(code, len(df1.index), len(df2.index)))
        pdb.set_trace()

#print_15min_vol_num(["600661"])

df = myapi.read_csv(r"stock2monitor-update.csv")
#df = dr5.get_a_across_b(df, period_of_days=1, cross_above=("close", "ma20"), cross_type="binary-cmp", period_type="week")
df1 = dr5.get_a_across_b(df, period_of_days=10*4*4, cross_above="volume", cross_type="unary-max",
                        period_type="15")
df1.p2 = df1.p2.astype("str")
df["volume"] = df1["p1"]
df["time"] = pd.to_datetime(df1["p2"], format='%Y%m%d%H%M%S%f')
df2 = df[df.time.dt.hour != 9]
df2 = df2.sort_values(by="time")
df2.to_csv("stock2monitor-volume-2.csv")
#pdb.set_trace()
#df.volume = df.volume.astype(int)
df.to_csv("stock2monitor-volume.csv")

df_vol = pd.DataFrame(index= df.index, columns=["lastvol", "lasttime", "curvol", "curtime", "delta"], dtype=int)
df_vol.curtime = df_vol.curtime.astype("string")
df_vol.lasttime =df_vol.lasttime.astype("string")
df_vol["maxvol"] = df["volume"]
df_vol["timemax"] = df["time"]
df_vol.to_csv("monitor-vol.csv")
df_vol.to_csv("monitor-vol-bak.csv")

#pdb.set_trace()