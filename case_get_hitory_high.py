import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb


stock_list_file = 'basic-no3.csv'
#stock_list_file = 'mystocklist-detail.csv'
df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})

"""
in latest 10 days, find history high
"""
df_result = myapi.get_history_high(df, 10)

df_result_final = df_result.loc[df_result['totals'] < 15]
df_result_final = df_result_final.loc[df_result['pe'] > 0]
df_result_final.to_csv(Path().joinpath('result', 'w-shape.csv'))
