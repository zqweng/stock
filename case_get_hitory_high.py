import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb

stock_list_file = 'basic-no3.csv'
# stock_list_file = 'mystocklist-detail.csv'
df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
df = myapi.remove_unwanted_fields(df)

"""
in latest 10 days, find history high
"""
df_result = myapi.get_history_high(df, 10, num_of_months=12)
print(df_result.to_string())
