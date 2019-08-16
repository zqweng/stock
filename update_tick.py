import pandas as pd
import tushare as ts
import os
import pdb
from pathlib import Path

"""
go to the tick_dir and create dir for 
"""


def load_tick(stock_list_file, start_date, end_date):
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})

    tick_dir = Path().joinpath('..', '..', 'stockdata','tick')
    timeRange = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d')

    for row in df.itertuples():
        dir_path = os.path.join(tick_dir, row.code)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print('Directory', os.path.join(tick_dir, row.code), 'Created')

        for date_val in timeRange:
            file_name = os.path.join(tick_dir, row.code, date_val + '.csv')
            if not os.path.exists(file_name):
                df_tick = ts.get_tick_data(row.code, date_val, src='tt')
                if df_tick is not None:
                    df_tick.to_csv(file_name)


if __name__ == "__main__":
    #load_tick('mystocklist-detail.csv', '2019-08-1', '2019-08-16')
    load_tick('basic-no3.csv','2019-08-1', '2019-08-16')
