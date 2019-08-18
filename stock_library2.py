import datetime
import os
import pandas as pd
from pathlib import Path
import pdb


def find_ma5_up(df, name,  code, latest_n_days, result_list):
    print ('find_ma5_up for ', code)
    ma5_cross_ma10 = False
    ma5_cross_ma20 = False
    for i in range(latest_n_days):
        if df.loc[i].ma10 == 0:
            return False

        if df.loc[i].ma5 <= df.loc[i+1].ma5:
            return False
        if df.loc[i].ma5 > df.loc[i].ma10 and df.loc[i+1].ma5 <= df.loc[i+1].ma10:
            ma5_cross_ma10 = True
        if df.loc[i].ma5 > df.loc[i].ma20 and df.loc[i + 1].ma5 <= df.loc[i + 1].ma20:
            ma5_cross_ma20 = True

    if ma5_cross_ma10 and ma5_cross_ma20:
        result_list.append(tuple((name, code, df.loc[0].date,
                                  df.loc[latest_n_days - 1].date,
                                  latest_n_days, 0)))
    return True

def hist_callback(stock_list_file, hist_dir, latest_n_days, callback, min_period=0):
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

        if stock_code == '600161':
            continue

        csv_file = stock_code + '.csv'
        if not os.path.exists(os.path.join(hist_dir, csv_file)):
            print('file', csv_file, 'does not exist, skip it')
            continue

        #stock_df = pd.read_csv(os.path.join(hist_dir, csv_file), nrows=latest_n_days + 1)
        stock_df = pd.read_csv(os.path.join(hist_dir, csv_file))

        if len(stock_df.index) < min_period:
            print('less than min period, discard it ', len(stock_df.index))
            continue

        if stock_df is None:
            print('failed to get history file ', stock_code)
            continue

        #pdb.set_trace()

        if len(stock_df.index) < latest_n_days + 1:
            continue

        callback(stock_df.head(latest_n_days + 1), stock_row.name, stock_code, latest_n_days, result_list)

    result_df = pd.DataFrame(result_list, columns=['name', 'code', 'start_date', 'end_date', 'days', 'p_change'])
    result_df.code = result_df.code.astype('str')

    print(start_time)
    print(datetime.datetime.now().time())
    return result_df


if __name__ == '__main__':
    result_string = ''
    tick_dir = Path().joinpath('..', '..', 'stockdata','week')
    # load_history(tick_dir, 'basic-no3.csv')
    result_df = hist_callback('basic-no3.csv', tick_dir, 5, find_ma5_up, 20)
    if not result_df.empty:
        result_string = result_string + "\n\nin last n days  ma5 up \n" + result_df.to_string()
    else:
        result_string = result_string + '\n\nno stock in last n days  has ma5 up \n'
    print(result_string)