import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb



df = myapi.get_latest_sum_of_week_price_up('basic-no3.csv', 2)
df = df.sort_values(by='p_change', ascending=False)
df = df.head(50)

num_of_weeks_ma10_go_up = 3
new_df = myapi.get_latest_n_periods_price_up(df, num_of_weeks_ma10_go_up, 'week', 'ma10')

str1 = df.to_string()
print(str1)
str2 = new_df.to_string()
print(str2)

