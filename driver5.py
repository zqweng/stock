import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb


def get_w_shape():
    stock_list_file = 'basic-no3.csv'
    #stock_list_file = 'mystocklist-detail.csv'
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    df_result = myapi.get_w_shape(df, 40)
    df_result.to_csv(Path().joinpath('result', 'w-shape.csv'))


def get_no_toch_ma5():
    stock_list_file = 'basic-no3.csv'
    # stock_list_file = 'mystocklist-detail.csv'
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    df_result = myapi.get_no_touch_ma5(df, 10)
    df_result.to_csv(Path().joinpath('result', 'no_touch_ma5.csv'))


