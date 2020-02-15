import time
import tushare as ts
import pandas as pd
import pdb

"""
df_stock = pd.read_csv('newlist.csv', converters={'code': lambda x: str(x)})

state_list = [[0 for x in range(5)] for y in range(len(df_stock.index))]

for i in range(len(df_stock.index)):
    state_list[i][0] = i
#stat_df = pd.DataFrame(state_list, columns=["code", "name", "bid-vol", "ask-vol", "ratio-bid-ask"])
stat_df = df_stock[["code", "name"]].copy()
count = 0
new_df = pd.DataFrame()
last_fetch_time = ''
stat_df['bidvol'] = 0
stat_df['askvol'] = 0
stat_df['ratio'] = 0.0
stat_df['p_change'] = 0.0
"""
#from live data file get real time bid/ask data for each stock and create a dataframe for each stock and do the following
# things:
# from stock list dataframe, import columns: code, name,
# from live data dataframe,
def create_stats_df():
    # read
    df = pandas.read_csv("live-data/realtime15.0.csv", converters={'code': lambda x: str(x)})
    df600529 = df[df["code"] == "600529"]
    df1 = df600529[["time", "volume", "price"]]
    df1['difvol'] = df1['volume'] - df1['volume'].shift(-1)
    df1['difprice'] = df1['price'] - df1['price'].shift(1)

def get_realtime_quote(list):
    global new_df
    global count
    global last_fetch_time
    df = ts.get_realtime_quotes(list)

    #if last_fetch_time == df.loc[0].time:
    #    return
    last_fetch_time = df.loc[0].time
    df.replace(to_replace='', inplace=True, value='0')

    print(df)

    b1_v = df.b1_v.astype("int32")
    b2_v = df.b2_v.astype("int32")
    b3_v = df.b3_v.astype("int32")
    b4_v = df.b4_v.astype("int32")
    b5_v = df.b5_v.astype("int32")
    a1_v = df.a1_v.astype("int32")
    a2_v = df.a2_v.astype("int32")
    a3_v = df.a3_v.astype("int32")
    a4_v = df.a4_v.astype("int32")
    a5_v = df.a5_v.astype("int32")
    col_preclose = df.pre_close.astype("float32")
    col_price = df.price.astype("float32")

    for i in range(len(df.index)):
        stat_df.at[i, 'bidvol'] = b1_v[i] + b2_v[i] + b3_v[i] + b4_v[i] + b5_v[i]
        stat_df.at[i, 'askvol'] = a1_v[i] + a2_v[i] + a3_v[i] + a4_v[i] + a5_v[i]
        stat_df.at[i, 'ratio'] = stat_df.loc[i].bidvol/stat_df.loc[i].askvol
        stat_df.at[i, "p_change"] = 100 * (col_price[i] - col_preclose[i])/col_preclose[i]

    print(stat_df.sort_values(by=['ratio'], ascending=False))
    a = df.loc[df['name'] == '思源电气']
    b = df.loc[0]
    print(type(b))
    print(type(a.b1_v.values[0]))
    print(a.volume.values[0])
    if df is not None:
        new_df = pd.concat([new_df, df])

    count = count + 1
    print('count is ', count)
    if count % 30 == 0:
        print('write a new file')
        # new_df.to_csv('realtime' + str(count/30) + '.csv')
        new_df = pd.DataFrame()


while True:
    get_realtime_quote(["000002", "600001"])
    time.sleep(10)
