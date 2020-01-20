
import pandas as pd
from pathlib import Path
import yfinance as yf
import stock_library3 as mylib3
import os
import pdb


# hist_dir = '/home/johnny/python/csv/'
# stock_list_file = 'mystocklist-detail.csv'


def update_history_with_callback(hist_dir, stock_list_file, callback, ktype_val='W'):
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})
        index = df['code']

    if ktype_val == 'D' or ktype_val == 'd':
        new_hist_dir = os.path.join(hist_dir, 'callback')
        hist_dir = os.path.join(hist_dir, 'day')
    elif ktype_val == 'W' or ktype_val == 'w':
        new_hist_dir = os.path.join(hist_dir, 'callback')
        hist_dir = os.path.join(hist_dir, 'week')
    elif ktype_val == 'W' or ktype_val == '60':
        new_hist_dir = os.path.join(hist_dir, 'callback')
        hist_dir = os.path.join(hist_dir, '60')

    if not os.path.exists(new_hist_dir):
        os.mkdir(new_hist_dir)

    total_num = len(index)
    cur_num = 1
    date_string = ''

    for stock_code in index:
        hist_file = os.path.join(hist_dir, stock_code + '.csv')
        new_hist_file = os.path.join(new_hist_dir, stock_code + '.csv')

        print(hist_file)
        if os.path.isfile(hist_file):
            df_stock_hist = pd.read_csv(hist_file, index_col='date')
        else:
            continue

        print('index is ', stock_code, 'cur is ', cur_num, 'total ', total_num)
        cur_num = cur_num + 1
        df_stock_hist = callback(df_stock_hist)
        df_stock_hist.to_csv(new_hist_file)


def find_sub_hist_dir(hist_dir, ktype_val):
    if ktype_val == 'D' or ktype_val == 'd':
        hist_dir = os.path.join(hist_dir, 'day')
    elif ktype_val == 'W' or ktype_val == 'w':
        hist_dir = os.path.join(hist_dir, 'week')
    elif ktype_val == 'M' or ktype_val == 'm':
        hist_dir = os.path.join(hist_dir, 'month')
    elif ktype_val == '60':
        hist_dir = os.path.join(hist_dir, '60')
    elif ktype_val == '15':
        hist_dir = os.path.join(hist_dir, '15')
    if not os.path.exists(hist_dir):
        os.mkdir(hist_dir)

    return hist_dir

"""
This function perform the following functions:
1: create a daatframe and fill the stock data into it
2: remove the row with zero volume
3: move the volume 'close' to the front of 'open' (reindex)
4: rename pctChg to p_change
"""
def modify_df_from_yahoo(df_result):
    df_result.rename(columns={"Open": "open", "High": "high", "Close": "close", "Volume": "volume", "Low": "low"}, inplace=True)
    df_result.index.names = ["date"]
    df_result = df_result.loc[df_result['volume'] != 0]
    df_result = df_result.dropna()
    return df_result

"""
if subdirectory 'week' or 'day' do not exist, it will create one.

"""
def load_history(hist_dir, stock_list_file, ktype_val='D'):

    default_start_date = '2019-07-01'

    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file)

    hist_dir = find_sub_hist_dir(hist_dir, ktype_val)

    total_num = len(df.index)
    cur_num = 1

    for stock_code in df['symbol']:
        #pdb.set_trace()
        hist_file = os.path.join(hist_dir, stock_code + '.csv')
        if os.path.isfile(hist_file):
            df_stock_hist = pd.read_csv(hist_file)
            date_string = (pd.to_datetime(df_stock_hist.loc[0].Date) + pd.to_timedelta('1 days')).strftime('%Y-%m-%d')
        else:
            df_stock_hist = pd.DataFrame()
            date_string = default_start_date

        print('index is ', stock_code, 'cur is ', cur_num, 'total ', total_num)
        cur_num = cur_num + 1

        df_from_network = yf.download(stock_code, start=date_string)

        if df_from_network.empty:
            print('no new data for', stock_code)
            continue

        df_from_network = modify_df_from_yahoo(df_from_network)

        if not df_stock_hist.empty:
            df_from_network = mylib3.ma_update(df_stock_hist.head(20).copy(), df_from_network)
            df_stock_joined = pd.concat([df_from_network, df_stock_hist])
            df_stock_joined.to_csv(hist_file)
        else:
            df_from_network = mylib3.ma(df_from_network)
            df_from_network = mylib3.boll(df_from_network)
            df_from_network.to_csv(hist_file)


if __name__ == "__main__":
    tick_dir = Path().joinpath('..', '..', 'us-stock-data')
    load_history(tick_dir, 'us_stock_volume.csv', 'd')
    #load_history_min(tick_dir, 'basic-no3.csv')
    #load_history_min(tick_dir, 'basic-no3.csv', ktype_val='15')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', add_boll, 'w')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', reset_columns, 'd')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', drop_zero_volume, 'd')
    #load_history(tick_dir, 'basic-no3.csv', 'w')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', add_ma_boll, '60')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', add_ma, '60')