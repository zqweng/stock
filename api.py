import datetime
import os
import pandas as pd
import stock_library2 as mylib2
import stock_library4 as mylib4
from pathlib import Path
import pdb


def get_latest_sum_of_week_price_up(stock_list_file, num_of_weeks):
    # stock_list_file = 'basic-no3.csv'
    # num_of_weeks = 2
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    if df.empty:
        print('no stock list, quit')
        quit()
    result_string = ''
    tick_dir = Path().joinpath('..', '..', 'stockdata', 'week')
    result_df = mylib2.hist_callback(df, tick_dir, num_of_weeks, mylib2.sum_of_latest_n_days_price_up,
                                     0,
                                     0,
                                     20)
    return result_df


def get_latest_n_periods_price_up(df, num_of_periods, type, period_type):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', 'stockdata', type)
    result_df = mylib2.hist_callback(df, tick_dir, num_of_periods, mylib2.find_price_go_up_for_n_period,
                                     period_type,
                                     0,
                                     20)
    return result_df

def fill_columns(df, df_result):
    df_result = df_result.reindex(columns=df_result.columns.tolist() + ['totals', 'pe'])
    for i in df_result.index:
        for row in df.itertuples():
            if df_result.loc[i].code == row.code:
                df_result.loc[i, 'totals'] = row.totals
                df_result.loc[i, 'pe'] = row.pe
    return df_result

def get_w_shape(df, num_of_periods, type='day'):
    result_string = ''
    tick_dir = Path().joinpath('..', '..', 'stockdata', type)
    df_result = mylib2.hist_callback(df, tick_dir, num_of_periods, mylib4.find_w_shape,
                                     0,
                                     0,
                                     num_of_periods)

    df_result = fill_columns(df, df_result)
    str_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    tmpfile = Path().joinpath('tmp', 'w-shape-' + str_time + '.csv')
    df_result.sort_values('start_date', inplace=True, ascending=False)
    df_result.to_csv(tmpfile)
    return df_result



