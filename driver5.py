import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb


def get_w_shape():
    stock_list_file = 'basic-no3.csv'
    #stock_list_file = 'mystocklist-detail.csv'
    df = myapi.read_csv(stock_list_file)
    df_result = myapi.get_w_shape(df, 40)
    df_result.to_csv(Path().joinpath('result', 'w-shape.csv'))


def get_no_toch_ma5():
    stock_list_file = 'basic-no3.csv'
    # stock_list_file = 'mystocklist-detail.csv'
    df = myapi.read_csv(stock_list_file)
    df_result = myapi.get_no_touch_ma5(df, 7)
    df_result.to_csv(Path().joinpath('result', 'no_touch_ma5.csv'))


def get_current_price_up_periods():
    stock_list_file = 'basic-no3.csv'
    # stock_list_file = 'mystocklist-detail.csv'
    df = myapi.read_csv(stock_list_file)
    df_result = myapi.get_current_price_up_periods(df)
    df_result.to_csv(Path().joinpath('result', 'current_price_up.csv'))

def get_current_no_touch_ma5_periods():
    stock_list_file = 'basic-no3.csv'
    # stock_list_file = 'mystocklist-detail.csv'
    df = myapi.read_csv(stock_list_file)
    df_result = myapi.get_current_no_touch_ma5_periods(df)
    df_result.to_csv(Path().joinpath('result', 'current_no_touch_ma5.csv'))

if __name__ == '__main__':
    #get_no_toch_ma5()
    #get_current_price_up_periods()
    get_current_no_touch_ma5_periods()