import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb


def get_w_shape():
    stock_list_file = 'basic-no3.csv'
    # stock_list_file = 'mystocklist-detail.csv'
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


def get_price_sum_in_n(df=None, is_price_up=True, price_up_sum=0, period_of_days=10, stock_list=None):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_price_sum_in_n(df, is_price_up, price_up_sum, period_of_days)

    return df_result

def get_price_continuous_down_in_n(df=None, price_down_sum=0, num_of_days_down=4, period_of_days=15):
    if df is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    df_result = myapi.get_price_continuous_down_in_n(df, num_of_days_down, price_down_sum, period_of_days)

    return df_result

def get_ma5_across_ma10(df=None, cross_above=True, period_of_days=10, stock_list=None):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_ma5_across_ma10(df, cross_above, period_of_days)

    return df_result

def get_price_above(df=None, type ="close above ma20", period_of_days=1, stock_list=None):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_price_above(df, type, period_of_days)

    return df_result

def get_price_up_with_percentage(df=None, p_change=4, period_of_days=10, stock_list=None):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_price_up_with_percentage(df, p_change, period_of_days)

    return df_result


if __name__ == '__main__':
    # get_no_toch_ma5()
    # get_current_price_up_periods()
    get_current_no_touch_ma5_periods()
