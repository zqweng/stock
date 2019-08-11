from pathlib import Path
import pandas as pd
import pdb

start_date = '2019-07-15'
end_date = '2019-07-19'
stock_list_file = 'mystocklist-detail.csv'

df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})

for row in df.itertuples():
    if row.name == '博通集成':
        """
        stock history file and stock tick file for each are under the same directory of ../../stockdata/stock_code/
        """
        stock_trade_file = row.code + '.csv'
        file_with_full_path = Path().joinpath('..', '..', 'stockdata', row.code, stock_trade_file)
        pdb.set_trace()
        df_stock = pd.read_csv(file_with_full_path, parse_dates=['date'])
        df_stock_new = df_stock[(df_stock['date'] >= start_date) & (df_stock['date'] <= end_date)]

