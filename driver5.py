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


def get_minimum_price_sum_in_n(df=None, is_price_up=True, price_up_sum=0, min_day_range=0, period_of_days=10, stock_list=None, period_type='day'):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_miminum_price_sum_in_n(df, is_price_up, price_up_sum, min_day_range, period_of_days, period_type)

    return df_result

def get_maximum_price_sum_in_n(df=None, p_change=(4,10), period_of_days=10, stock_list=None, period_type='day'):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_maximum_price_sum_in_n(df, p_change, period_of_days, period_type)

    return df_result

def get_price_continuous_down_in_n(df=None, price_down_sum=0, num_of_days_down=4, period_of_days=15, period_type='day'):
    if df is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    df_result = myapi.get_price_continuous_down_in_n(df, num_of_days_down, price_down_sum, period_of_days, period_type)

    return df_result

def get_a_across_b(df=None, cross_above=True, cross_type="ma5-ma10", period_of_days=10, stock_list=None, period_type='day'):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_a_across_b(df, cross_above, cross_type, period_of_days, period_type)

    return df_result

def get_price_above(df=None, type ="close above ma20", period_of_days=1, stock_list=None, period_type='day'):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_price_above(df, type, period_of_days, period_type)

    return df_result

def get_price_up_with_percentage(df=None, p_change=(4,10), period_of_days=10, stock_list=None, period_type='day'):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_price_up_with_percentage(df, p_change, period_of_days, period_type)

    return df_result

def get_latest_n_periods_price_up(df=None, period_of_days=10, stock_list=None, period_type='day'):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        # stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_latest_n_periods_price_up(df, p_change, period_of_days, period_type)

    return df_result

def get_maximum_period_break_high(df=None, min_break_num=4, period_of_days=10, stock_list=None, period_type='day'):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        #stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_maximum_period_break_high(df, min_break_num, period_of_days, period_type)

    return df_result

def get_history_high_price(df=None, event_to_now = 1, period_of_days=60, stock_list=None, period_type='day'):
    if df is None and stock_list is None:
        stock_list_file = 'basic-no3.csv'
        #stock_list_file = 'mystocklist-detail.csv'
        df = myapi.read_csv(stock_list_file)
    else:
        if stock_list is not None:
            df = myapi.read_csv(stock_list)
    df_result = myapi.get_history_high_price(df, event_to_now, period_of_days, period_type)

    return df_result

if __name__ == '__main__':
    # get_no_toch_ma5()
    # get_current_price_up_periods()
    get_current_no_touch_ma5_periods()
