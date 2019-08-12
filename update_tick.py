import pandas as pd
import tushare as ts
import os
import pdb
"""
go to the tick_dir and create dir for 
"""

def load_tick(tick_dir, stock_list_file, start_date, end_date):
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})

    for row in df.itertuples():
       if not os.path.exists(os.path.join(tick_dir,row.code)):
            os.mkdir(os.path.join(tick_dir,row.code))
            print('Directory', os.path.join(tick_dir,row.code), 'Created')

        tick_df = ts.get_tick_data(stock_code, date=date_val, src='tt')

        if tick_df is None:
            print('history data on date ', date_val, 'for stock', stock_code, 'failed to retrieve')
            continue

        tick_df.to_csv(date_val + '.csv')




