"""
when you import
"""
import os
import pandas as pd
import update_history
import stock_library as mylib
from pathlib import Path
import pdb

result_string = ''
# pdb.set_trace()

#stock_list_file = 'mystocklist-detail.csv'
stock_list_file = 'basic-no3.csv'
history_dir = Path().joinpath('..', '..', 'stockdata','day')
#update_history.load_history(history_dir, stock_list_file)

df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})

if df.empty:
    print('no stock list, quit')
"""
result_df = mylib.day_k_cross(df, history_dir, 2)
# pdb.set_trace()
if not result_df.empty:
    result_string = result_string + '\nma5 cross ma10 \n' + result_df.to_string()
else:
    result_string = result_string + '\nno ma5 cross ma10 \n'
"""
result_df1 = mylib.day_price_calculate(df, history_dir, 5, 'break ma')
if not result_df1.empty:
    result_string = result_string + '\n\nprice break ma5 and ma10 \n' + result_df1.to_string()
else:
    result_string = result_string + '\n\n no price break ma5 and ma10 \n'

result_df2 = mylib.day_price_calculate(df, history_dir, 2, 'lower shadow')
if not result_df.empty:
    result_string = result_string + '\n\nprice has a lower shadow line ratio > 2 \n' + result_df2.to_string()
else:
    result_string = result_string + '\n\nno price has a lower shadow line ratio > 2 \n'
print(result_string)

df_common = result_df[result_df['code'].isin(result_df1['code'])]
df_common = result_df2[result_df2['code'].isin(df_common['code'])]
if not df_common.empty:
    print('\n\n common stock \n' + df_common.to_string())