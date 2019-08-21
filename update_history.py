"""
Update the stock history files specified by stock_list_file with the latest trading record. It checks the local trading
record first and append latest record retrieved from network to the existing file.
stock history files are not stored in git.
1 load the stock list
2 iterating through stock list, load each stock trade file.
3 the date element in dataframe is a string type. we need to do an adding one day operation and retrieve
   the record since that latest day
4 the dataframe created by reading file has been added a new index column by pandas, this index is the row number
   so we can use this index to access each row by df.loc[index]. when  writing back to csv file, this index will be kept
   in the file. So if we dont want this index in fhe file, we should set index to date before we write
5  the dataframe read from the network has date as index, so when it write to csv file, no extra index is added.

6  we need to use pandas.concat to combine the two dataframe, before joining them together, we should remove the index
   columen in the dataframe from file.

7  when we write back of new dataframe to the opened file, the old content will be overwritten.
"""

import pandas as pd
from pathlib import Path
import tushare as ts
import os


# hist_dir = '/home/johnny/python/csv/'
# stock_list_file = 'mystocklist-detail.csv'

def load_history(hist_dir, stock_list_file, ktype_val='D'):
    default_start_date = ''
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})
        index = df['code']
    if ktype_val == 'D' or ktype_val == 'd':
        hist_dir = os.path.join(hist_dir, 'day')
    elif ktype_val == 'W' or ktype_val == 'w':
        hist_dir = os.path.join(hist_dir, 'week')
    if not os.path.exists(hist_dir):
        os.mkdir(hist_dir)
    #os.chdir(hist_dir)

    total_num = len(index)
    cur_num = 1
    date_string = ''

    for stock_code in index:
        # df_stock_hist = pd.read_csv(stock_code + '.csv', parse_dates=['date'])
        hist_file = os.path.join(hist_dir, stock_code + '.csv')
        if os.path.isfile(hist_file):
            df_stock_hist = pd.read_csv(hist_file)
        else:
            df_stock_hist = pd.DataFrame()

        if not df_stock_hist.empty:
            date_string = (pd.to_datetime(df_stock_hist.loc[0].date) + pd.to_timedelta('1 days')).strftime('%Y-%m-%d')
        else:
            date_string = default_start_date

        print('index is ', stock_code, 'cur is ', cur_num, 'total ', total_num)
        cur_num = cur_num + 1

        df_from_network = ts.get_hist_data(stock_code, start=date_string, ktype=ktype_val)
        if df_from_network is None:
            print('fail get history file', stock_code)
            continue
        if df_from_network.empty:
            print('no new data for', stock_code)
            continue

        if not df_stock_hist.empty:
            df_stock_hist.set_index('date', inplace=True)

        df_stock_joined = pd.concat([df_from_network, df_stock_hist])

        df_stock_joined.to_csv(hist_file)


if __name__ == "__main__":
    tick_dir = Path().joinpath('..', '..', 'stockdata')
    #'mystocklist-detail.csv'
    load_history(tick_dir, 'basic-no3.csv')
    #load_history(tick_dir, 'basic-no3.csv')
    #load_history(tick_dir, 'basic-no3.csv', 'W')
