import datetime
import os
import pandas as pd
import numpy as np
import stock_library2 as mylib2
import stock_library4 as mylib4
import stock_library5 as mylib5
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
import pdb

def get_data_dir():
    return 'stockdata-bao'

def get_latest_sum_of_week_price_up(stock_list_file, num_of_weeks):
    # stock_list_file = 'basic-no3.csv'
    # num_of_weeks = 2
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    if df.empty:
        print('no stock list, quit')
        quit()
    result_string = ''
    tick_dir = Path().joinpath('..', '..', get_data_dir(), 'week')
    result_df = mylib2.hist_callback(df, tick_dir, num_of_weeks, mylib2.sum_of_latest_n_days_price_up,
                                     0,
                                     0,
                                     20)
    return result_df


def get_latest_n_periods_price_up(df, num_of_periods, type, period_type):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', get_data_dir(), type)
    result_df = mylib2.hist_callback(df, tick_dir, num_of_periods, mylib2.find_price_go_up_for_n_period,
                                     period_type,
                                     0,
                                     20)
    return result_df


def fill_columns(df, df_result):
    print('start filling columns')
    start_time = datetime.datetime.now().time()
    df_result = df_result.reindex(columns=df_result.columns.tolist() + ['totals', 'pe'])
    for i in df_result.index:
        if df_result.loc[i].code in df.index:
            df_result.loc[i, 'totals'] = df.loc[df_result.loc[i].code].totals
            df_result.loc[i, 'pe'] = df.loc[df_result.loc[i].code].pe
    print('end filing columns')
    print(start_time)
    print(datetime.datetime.now().time())
    return df_result


def rank_stock(df_result):
    print('start ranking')
    start_time = datetime.datetime.now().time()
    df_result = df_result.replace({'pe': 0}, 10000)
    df_result = df_result[df_result['totals'] != 0]
    df_result['rank'] = 5 / np.log10(df_result['pe']) + 2 / np.log10(3 * df_result['totals'])
    df_result['rankPe'] = 5 / np.log10(df_result['pe'])
    df_result['ranktotals'] = 2 / np.log10(3 * df_result['totals'])
    df_result.sort_values('rank', inplace=True, ascending=False)
    print('end ranking')
    print(start_time)
    print(datetime.datetime.now().time())
    return df_result


def get_w_shape(df, num_of_periods, type='day'):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', get_data_dir(), type)
    df_result = mylib2.hist_callback(df, tick_dir, num_of_periods, mylib4.find_w_shape,
                                     0,
                                     0,
                                     num_of_periods)

    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    df_result = rank_stock(df_result)
    tmpfile = Path().joinpath('tmp', 'w-shape-' + str_time + '.csv')
    df_result.to_csv(tmpfile)
    return df_result


def get_history_high(df, num_of_days, num_of_months=0):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', get_data_dir(), 'day')
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days, mylib4.find_history_high,
                                     num_of_days,
                                     num_of_months,
                                     60)

    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_history_high-' + str_time + '_' + str(num_of_months) + '_mon_' + '.csv')
    df_result = rank_stock(df_result)
    df_result.to_csv(tmpfile)
    return df_result

"""
   This function calculate history high from day trading table instead of month trading table
"""
def get_history_high_v2(df, num_of_days, num_of_days_periods=0):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', get_data_dir(), 'day')
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib4.find_history_high_v2,
                                     num_of_days,
                                     0,
                                     60)

    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_history_high_v2-' + str_time + '_' + str(num_of_days_periods) + '_days_' + '.csv')
    df_result = rank_stock(df_result)
    df_result.to_csv(tmpfile)
    return df_result

def remove_unwanted_fields(df):
    return df.loc[(df['industry'] != '银行') & (df['industry'] != '白酒')]


def get_no_touch_ma5(df, num_of_days):
    tick_dir = Path().joinpath('..', '..', get_data_dir(), 'day')
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days, mylib4.find_price_up_and_no_touch_ma5_for_n_period,
                                     num_of_days,
                                     0,
                                     60)

    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_no_touch_ma5-' + str_time + '.csv')
    df_result = rank_stock(df_result)
    df_result.sort_values('days', inplace=True, ascending=False)
    df_result.to_csv(tmpfile)
    return df_result


def get_current_price_up_periods(df):
    tick_dir = Path().joinpath('..', '..', get_data_dir(), 'day')
    df_result = mylib2.hist_callback(df, tick_dir, 60, mylib5.find_current_price_up_for_n_period,
                                     60,
                                     0,
                                     60)
    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_no_touch_ma5-' + str_time + '.csv')
    df_result = rank_stock(df_result)
    df_result.sort_values('days', inplace=True, ascending=False)
    df_result.to_csv(tmpfile)
    return df_result

def get_current_no_touch_ma5_periods(df):
    tick_dir = Path().joinpath('..', '..', get_data_dir(), 'day')
    df_result = mylib2.hist_callback(df, tick_dir, 60, mylib5.find_current_no_touch_ma5_for_n_period,
                                     60,
                                     0,
                                     60)
    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_current_no_touch_ma5-' + str_time + '.csv')
    df_result = rank_stock(df_result)
    df_result.sort_values('days', inplace=True, ascending=False)
    df_result.to_csv(tmpfile)
    return df_result

def read_csv(stock_list_file):
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    df.set_index('code', inplace=True)
    return df



"""
   This function calculate history high from day trading table instead of month trading table
"""
def get_history_high_volume(df, num_of_days, num_of_days_periods=0):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', get_data_dir(), 'day')
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib4.find_history_high_volume,
                                     num_of_days,
                                     0,
                                     60)

    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_history_high_volume-' + str_time + '_' + str(num_of_days_periods) + '_days_' + '.csv')
    df_result = rank_stock(df_result)
    df_result.to_csv(tmpfile)
    return df_result

"""
   This function calculate history high from day trading table instead of month trading table
"""
def get_first_history_high_volume_in_n(df, num_of_days, num_of_days_periods=0):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', get_data_dir(), 'day')
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib4.find_first_history_high_volume,
                                     num_of_days,
                                     0,
                                     60)

    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_first_history_high_volume-' + str_time + '_' + str(num_of_days_periods) + '_days_' + '.csv')
    df_result = rank_stock(df_result)
    df_result.to_csv(tmpfile)
    return df_result