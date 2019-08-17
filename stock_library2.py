import datetime
import os
import pandas as pd
from pathlib import Path
import pdb


def find_ma5_up(df, code, latest_n_days, result_list):
    print ('find_ma5_up for ', code)
    for i in range(latest_n_days):
        #pdb.set_trace()
        if df.loc[i].ma5 <= df.loc[i+1].ma5:
            return False

    return True

def hist_callback(stock_list_file, hist_dir, latest_n_days, callback):
    """
    current criteria is
    find up period list

    :param stock_list_file:
    :param df: dataframe includes the stock list to be analyzed
    :param hist_dir: stock history files for the stock list
    :param latest_n_days:
    :return: a new dataframe that meet the criteria.
    """

    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})

    if df.empty:
        print('no stock list, quit')
        return

    start_time = datetime.datetime.now().time()
    stock_num = 0
    result_list = []

    for stock_row in df.itertuples():
        stock_code = stock_row.code
        print('index is ', stock_code, 'num of stock is ', stock_num)
        stock_num = stock_num + 1

        csv_file = stock_code + '.csv'
        if not os.path.exists(os.path.join(hist_dir, csv_file)):
            print('file', csv_file, 'does not exist, skip it')
            continue

        stock_df = pd.read_csv(os.path.join(hist_dir, csv_file), nrows=latest_n_days + 1)

        if stock_df is None:
            print('failed to get history file ', stock_code)
            continue

        #pdb.set_trace()

        if len(stock_df.index) < latest_n_days + 1:
            continue

        callback(stock_df, stock_code, latest_n_days, result_list)

    result_df = pd.DataFrame(result_list, columns=['code', 'start_date', 'end_date', 'days', 'p_change'])
    result_df.code = result_df.code.astype('str')

    print(start_time)
    print(datetime.datetime.now().time())
    return result_df


if __name__ == '__main__':
    tick_dir = Path().joinpath('..', '..', 'stockdata','week')
    # load_history(tick_dir, 'basic-no3.csv')
    result_df = hist_callback('basic-no3.csv', tick_dir, 5, find_ma5_up)
    if not result_df.empty:
        result_string = result_string + "\n\nin last n days  ma5 up \n" + result_df.to_string()
    else:
        result_string = result_string + '\n\nno stock in last n days  has ma5 up \n'
    print(result_string)