"""
  function summary:
  1: handling two kinds of files: stock_code.csv and its relates date.csv. assume they are located
     under the directory of ../../stockdata/stock_code.
  2: use pathlib to generate a os independant path
  2: subset dataframe between a start/end date
  4: resample the dataframe
  5: concanate the dataframe


"""

from pathlib import Path
import os
import pandas as pd
from utils import drawing_library as mydraw, stock_library as mylib
import pdb

start_date = '2019-01-1'
end_date = '2019-08-25'
stock_list_file = 'mystocklist-detail.csv'
resample_intv = '60min'

df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})
#stock_name = '三全食品'
stock_name = '博通集成'
#stock_name = '金健米业'
for row in df.itertuples():
    if row.name == stock_name:
        """
        stock history file and stock tick file for each are under the same directory of ../../stockdata/stock_code/
        """
        stock_trade_file = row.code + '.csv'
        file_path = Path().joinpath('..', '..', 'stockdata','day')
        file_with_full_path = os.path.join(file_path,stock_trade_file)
        #pdb.set_trace()
        df_stock = pd.read_csv(file_with_full_path, parse_dates=['date'])
        df_stock_new = df_stock[(df_stock['date'] >= start_date) & (df_stock['date'] <= end_date)]
        df_general = pd.DataFrame()

        # cannot use (row_new in df_stock_new)
        for row_new in df_stock_new.itertuples():
            date_val = row_new.date.strftime('%Y-%m-%d')
            tick_file_name = date_val + '.csv'
            tick_file_with_full_path = os.path.join(file_path, row.code, tick_file_name)
            df_tick = pd.read_csv(tick_file_with_full_path)
            #pdb.set_trace()
            if df_tick.empty:
                print('empty tick for date ', tick_file_name)
                break
            else:
                pdb.set_trace()
                df_resample = mylib.resample(df_tick, resample_intv, date_val)
                #pdb.set_trace()
                if df_resample is not None:
                    """
                    Concanate needs a list of dataframe as input 
                    """
                    df_general = pd.concat([df_general, df_resample])

        if not df_general.empty:
            df_general.sort_index(ascending=1, inplace=True)
            pdb.set_trace()
            mydraw.draw_k_lines(df_general)







