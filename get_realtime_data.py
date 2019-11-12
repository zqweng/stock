import time
import tushare as ts
import pandas as pd
import pdb

df_stock = pd.read_csv('mystocklist-detail.csv', converters={'code': lambda x: str(x)})
count = 0
new_df = pd.DataFrame()

def get_realtime_quote():
    global new_df
    global count
    df = ts.get_realtime_quotes(df_stock['code'])
    print(df)
    if df is not None:
        new_df = pd.concat([new_df, df])

    count = count + 1
    print('count is ', count)
    if count % 30 == 0:
        print('write a new file')
        new_df.to_csv('realtime' + str(count/30) + '.csv')
        new_df = pd.DataFrame()


while True:
    get_realtime_quote()
    time.sleep(10)