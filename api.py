import datetime
import pandas as pd
import numpy as np
import stock_library2 as mylib2
from utils import stock_library4 as mylib4, stock_library5 as mylib5
import stock_library6 as mylib6
from pathlib import Path
import platform

market = "China"
def get_data_dir():
    if market == "China":
        return 'stockdata-bao'
    else:
        return 'us-stock-data'

def getPath(period_type):
    if platform.system() == "Windows":
        path = Path("C:/Users/johnny/")
    return path/get_data_dir()/period_type

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

def add_columns(df_result):
    df = read_csv("basic-no3.csv")
    if df.empty:
        print('no stock list, quit')
        quit()

    print('start filling columns')

    start_time = datetime.datetime.now().time()
    df_result = df_result.reindex(columns=df_result.columns.tolist() + ['totals', 'pe'])

    for i in df_result.index:
        if df_result.loc[i].code in df.index:
            df_result.loc[i, 'outstanding'] = df.loc[df_result.loc[i].code].outstanding
            df_result.loc[i, 'totals'] = df.loc[df_result.loc[i].code].totals
            df_result.loc[i, 'pe'] = df.loc[df_result.loc[i].code].pe

    print('end filing columns')
    print(start_time)
    print(datetime.datetime.now().time())
    return df_result


def add_columns_and_rank_stock(df_result):
    df = read_csv("basic-no3.csv")
    if df.empty:
        print('no stock list, quit')
        quit()

    print('start filling columns')

    start_time = datetime.datetime.now().time()
    df_result = df_result.reindex(columns=df_result.columns.tolist() + ['totals', 'pe'])

    for i in df_result.index:
        if df_result.loc[i].code in df.index:
            df_result.loc[i, 'outstanding'] = df.loc[df_result.loc[i].code].outstanding
            df_result.loc[i, 'totals'] = df.loc[df_result.loc[i].code].totals
            df_result.loc[i, 'pe'] = df.loc[df_result.loc[i].code].pe

    print('end filing columns')
    print(start_time)
    print(datetime.datetime.now().time())
    return rank_stock(df_result)

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

def read_csv(stock_list_file, local=False):
    if not local and platform.system() == "Windows":
        file = Path("C:/Users/johnny/PycharmProjects/stock-github")/stock_list_file
    else:
        file = stock_list_file
    df = pd.read_csv(file, converters={'code': lambda x: str(x)})
    if market == "China":
        df.set_index('code', inplace=True)
    else:
        df.set_index('code', inplace=True)
    df["ret"] = 0
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

"""
   This function calculate history high from day trading table instead of month trading table
"""
def get_miminum_price_sum_in_n(df, is_price_up, min_price_range, min_day_range, num_of_days_periods, period_type):
    tick_dir = getPath(period_type)
    result_list = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib6.find_minimum_price_sum_for_n_period,
                                     is_price_up,
                                     (min_price_range, min_day_range),
                                     60)

    df_result = pd.DataFrame(result_list,
                             columns=['name', 'code', 'start_date', 'end_date', 'days', 'p_change'])
    df_result.code = df_result.code.astype('str')
    #df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_price_sum_in_n-' + period_type + str_time + '_' + str(num_of_days_periods) + '_days_' + '.csv')
    #df_result = rank_stock(df_result)
    #pdb.set_trace()
    df_result.sort_values('p_change', inplace=True, ascending=not is_price_up)
    df_result.set_index('code', inplace=True)
    df_result.to_csv(tmpfile)
    return df_result

def get_maximum_price_sum_in_n(df, percentage, num_of_days_periods, period_type):
    result_string = ''
    tick_dir = getPath(period_type)
    result_list = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib6.find_maximum_price_sum_for_n_period,
                                     percentage,
                                     0,
                                     60)

    df_result = pd.DataFrame(result_list, columns=['name', 'code', 'start_date', 'end_date', 'days', 'p_change'])
    df_result.code = df_result.code.astype('str')

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_maximum_price_sum_in_n-' + period_type + '_' + str(num_of_days_periods) + '_days_' + str_time + '.csv')
    #df_result = rank_stock(df_result)
    #pdb.set_trace()
    df_result.set_index('code', inplace=True)
    df_result.to_csv(tmpfile)
    return df_result


"""
   This function calculate history high from day trading table instead of month trading table
"""
def get_price_continuous_down_in_n(df, num_of_days_down, price_down_sum, num_of_days_periods, period_type):
    result_string = ''
    tick_dir = getPath(period_type)
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib6.find_price_continuous_down_for_n_period,
                                     num_of_days_down,
                                     price_down_sum,
                                     60)

    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_price_continuous_down_in_n-' + period_type  + str_time + '_' + str(num_of_days_periods) + '_days_' + '.csv')
    df_result = rank_stock(df_result)
    df_result.to_csv(tmpfile)
    return df_result

"""
   This function calculate history high from day trading table instead of month trading table
"""
def get_a_across_b(df, cross_above, cross_type, num_of_days_periods, period_type, rank):
    result_string = ''
    tick_dir = getPath(period_type)
    result_list = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib6.find_a_cross_b,
                                     cross_above,
                                     cross_type,
                                     30)

    df_result = pd.DataFrame(result_list, columns=['name', 'code', 'start_date', 'end_date', 'days', 'p_change', 'p1', 'p2', 'p3'])
    df_result.code = df_result.code.astype('str')

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_a_across_b-' + str(mylib2.head_offset) + '_' + period_type + cross_type + '_' + str(num_of_days_periods) + '_days_' + "-" + str_time + '.csv')
    df_result = add_columns(df_result)
    df_result.set_index('code', inplace=True)
    df_result.to_csv(tmpfile)
    return df_result

def get_price_above(df, type, num_of_days_periods, period_type):
    result_string = ''
    tick_dir = getPath(period_type)
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib6.find_price_above,
                                     type,
                                     0,
                                     60)

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_price_above-' + period_type + '_' + str(num_of_days_periods) + '_days_' + '.csv')
    #df_result = rank_stock(df_result)
    #pdb.set_trace()
    df_result.set_index('code', inplace=True)
    df_result.to_csv(tmpfile)
    return df_result

def get_price_up_with_percentage(df, percentage, num_of_days_periods, period_type):
    result_string = ''
    tick_dir = getPath(period_type)
    result_list = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib6.find_price_up_with_percentage,
                                     percentage,
                                     0,
                                     60)

    df_result = pd.DataFrame(result_list,
                             columns=['name', 'code', 'start_date', 'end_date', 'days', 'p_change'])
    df_result.code = df_result.code.astype('str')

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_price_up_with_percentage-' + period_type + '_' + str(num_of_days_periods) + '_days_' + str_time + '.csv')
    #df_result = rank_stock(df_result)
    #pdb.set_trace()
    df_result.set_index('code', inplace=True)
    df_result.to_csv(tmpfile)
    return df_result



def get_latest_n_periods_price_up(df, num_of_periods, type, period_type):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', get_data_dir(), type)
    result_df = mylib2.hist_callback(df, tick_dir, num_of_periods, mylib2.find_price_go_up_for_n_period,
                                     period_type,
                                     0,
                                     20)
    return result_df

def get_maximum_period_break_high(df, min_break_num, num_of_days_periods, period_type):
    result_string = ''
    tick_dir = getPath(period_type)
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib5.find_maximum_period_break_high,
                                     min_break_num,
                                     0,
                                     60)

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_maximum_period_break_high-' + period_type + '_' + str(num_of_days_periods) + '_days_' + str_time + '.csv')
    #df_result = rank_stock(df_result)
    #pdb.set_trace()
    df_result.set_index('code', inplace=True)
    df_result.to_csv(tmpfile)
    return df_result

def get_history_high_price(df, event_to_now, num_of_days_periods, period_type):
    tick_dir = getPath(period_type)
    df_result = mylib2.hist_callback(df, tick_dir, num_of_days_periods, mylib4.find_history_high_v2,
                                     event_to_now,
                                     0,
                                     60)

    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'get_history_high_price-' + str_time + '_' + str(num_of_days_periods) + '_days_' + '.csv')
    df_result.set_index('code', inplace=True)
    df_result.to_csv(tmpfile)
    return df_result