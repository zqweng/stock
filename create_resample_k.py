import os
import pandas as pd
from pathlib import Path
import stock_library as mylib
import pdb

def create_resample_k(stock_list_file, start_date, end_date, resample_intv):

    df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})

    tick_dir = Path().joinpath('..', '..', 'stockdata', 'tick')
    timeRange = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d')

    result_dir = os.path.join('..', '..', 'stockdata', resample_intv)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    for row in df.itertuples():
        dir_path = os.path.join(tick_dir, row.code)
        if not os.path.exists(dir_path):
            print('Directory', dir_path, 'not exist')
            quit()

        df_resample_k = pd.DataFrame()

        for date_val in timeRange:
            file_name = os.path.join(dir_path, date_val + '.csv')
            if os.path.exists(file_name):
                df_tick = pd.read_csv(file_name)
                if not df_tick.empty:
                    df_tick = mylib.resample(df_tick, resample_intv, date_val)
                df_resample_k = pd.concat([df_resample_k,df_tick])

        df_resample_k['ma5'] = df_resample_k.close.rolling(window=5, min_periods=1).mean()
        df_resample_k = df_resample_k.round(2)
        df_resample_k.index.names = ['date']
        result_file_name = os.path.join(result_dir, row.code + '.csv')
        print ('write result file', result_file_name)
        df_resample_k.to_csv(result_file_name)

if __name__ == "__main__":
    create_resample_k('mystocklist-detail.csv', '2019-07-08', '2019-07-30','60min')