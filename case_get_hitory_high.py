import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb

def get_one_year_high():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_one_year_high.csv')

    # stock_list_file = 'mystocklist-detail.csv'
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_history_high(df, 10, 12)
    df_result.to_csv(tmpfile)

def get_history_high():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_history_high.csv')
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_history_high(df, 10)
    df_result.to_csv(tmpfile)
