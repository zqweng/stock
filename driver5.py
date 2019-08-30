import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb

stock_list_file = 'basic-no3.csv'
df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
df_result = myapi.get_w_shape(df, 40)

df_result.to_csv(Path().joinpath('result', 'w-shape.csv'))
str1 = df_result.to_string()
print(str1)
