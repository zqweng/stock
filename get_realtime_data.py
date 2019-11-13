import time
import tushare as ts
import pandas as pd
import pdb

df_stock = pd.read_csv('newlist.csv', converters={'code': lambda x: str(x)})
count = 0
new_df = pd.DataFrame()
stat_df = pd.DataFrame(columns=["code", "name", "bid-vol", "ask-vol", "ratio-bid-ask"])
state_list = [[0 for x in range(4)] for y in range(len(df_stock.index))]
for i in range(len(df_stock.index)):
    state_list[i][0] = i
print(state_list)
def get_realtime_quote():
    global new_df
    global count
    df = ts.get_realtime_quotes(df_stock['code'])

    for i in range(len(df.index)):
        b1_all = df.loc[i].b1_v + df.loc[i].b2_v + df.loc[i].b3_v + df.loc[i].b4_v + df.loc[i].b5_v
        a1_all = df.loc[i].a1_v + df.loc[i].a2_v + df.loc[i].a3_v + df.loc[i].a4_v + df.loc[i].a5_v
        state_list[i][2] += b1_all
        state_list[i][3] += a1_all

    print(state_list)
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
        #new_df.to_csv('realtime' + str(count/30) + '.csv')
        new_df = pd.DataFrame()


while True:
    get_realtime_quote()
    time.sleep(10)