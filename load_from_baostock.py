
import pandas as pd
from pathlib import Path
import baostock as bs
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
def create_df_from_bao_rs(rs):
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

    df_result = pd.DataFrame(data_list, columns=rs.fields)
    df_result = df_result.loc[df_result['volume'] != '0']
    if len(df_result.index) == 0:
        return None

    df_result = df_result[['date', 'open', 'high', 'low', 'close', 'volume', 'turn', 'pctChg']]
    df_result.set_index('date', inplace=True)
    #df_result.sort_index(ascending=False, inplace=True)
    columns = ['close', 'open', 'high', 'low', 'volume', 'turn', 'pctChg']
    df_result = df_result.reindex(columns=columns)
    df_result.columns = ['close', 'open', 'high', 'low', 'volume', 'turn', 'p_change']
    return df_result

"""
This function perform the following functions:
1: create a daatframe and fill the stock data into it
2: remove the row with zero volume
3: move the volume 'close' to the front of 'open' (reindex)
4: rename pctChg to p_change
"""
def create_df_from_bao_rs_min(rs):
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())

    df_result = pd.DataFrame(data_list, columns=rs.fields)
    df_result = df_result.loc[df_result['volume'] != '0']
    if len(df_result.index) == 0:
        return None

    df_result = df_result[['date', 'time', 'open', 'high', 'low', 'close', 'volume']]
    df_result.set_index(['date', 'time'], inplace=True)
    df_result.sort_index(ascending=False, inplace=True)
    columns = ['close', 'open', 'high', 'low', 'volume', 'amount']
    df_result = df_result.reindex(columns=columns)
    df_result.columns = ['close', 'open', 'high', 'low', 'volume', 'amount']
    return df_result

"""
change 6xxxxx to sh.6xxxxx, 0xxxxx to sz.0xxxxxxx
"""
def add_stock_code_prefix(code):
    if code[0] == '6':
        return 'sh.' + code
    else:
        return 'sz.' + code


"""
if subdirectory 'week' or 'day' do not exist, it will create one.

"""
def load_history(hist_dir, stock_list_file, ktype_val='D'):
    lg = bs.login()

    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    default_start_date = '2009-01-01'
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})

    hist_dir = find_sub_hist_dir(hist_dir, ktype_val)

    total_num = len(df.index)
    cur_num = 1

    for stock_code in df['code']:
        # df_stock_hist = pd.read_csv(stock_code + '.csv', parse_dates=['date'])
        hist_file = os.path.join(hist_dir, stock_code + '.csv')
        if os.path.isfile(hist_file):
            df_stock_hist = pd.read_csv(hist_file)
        else:
            df_stock_hist = pd.DataFrame()

        if not df_stock_hist.empty:
            date_string = (pd.to_datetime(df_stock_hist.loc[0].date) + pd.to_timedelta('1 days')).strftime('%Y-%m-%d')
        else:
            date_string = default_start_date

        print('index is ', stock_code, 'cur is ', cur_num, 'total ', total_num)
        cur_num = cur_num + 1

        rs = bs.query_history_k_data_plus(add_stock_code_prefix(stock_code),
                                          "date,code,open,high,low,close,volume,turn,pctChg",
                                          start_date=date_string,
                                          frequency=ktype_val, adjustflag="2")
        if len(rs.data) == 0:
            print('no new data for', stock_code)
            continue

        df_from_network = create_df_from_bao_rs(rs)


        if df_from_network is None:
            print('discard idle data')
            continue

        df_from_network = df_from_network[df_from_network.turn != '']

        if not df_stock_hist.empty:
            df_stock_hist.set_index('date', inplace=True)
            df_from_network = mylib3.ma_update(df_stock_hist.head(20).copy(), df_from_network)
            df_stock_joined = pd.concat([df_from_network, df_stock_hist])
            df_stock_joined.to_csv(hist_file)
        else:
            df_from_network = mylib3.ma(df_from_network)
            df_from_network.to_csv(hist_file)

        #pdb.set_trace()

"""
if subdirectory 'week' or 'day' do not exist, it will create one.

"""
def load_history_min(hist_dir, stock_list_file, ktype_val='60'):
    lg = bs.login()

    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    default_start_date = '2019-12-31'
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})

    hist_dir = find_sub_hist_dir(hist_dir, ktype_val)

    total_num = len(df.index)
    cur_num = 1

    for stock_code in df['code']:
        # df_stock_hist = pd.read_csv(stock_code + '.csv', parse_dates=['date'])
        hist_file = os.path.join(hist_dir, stock_code + '.csv')
        if os.path.isfile(hist_file):
            df_stock_hist = pd.read_csv(hist_file)
        else:
            df_stock_hist = pd.DataFrame()

        if not df_stock_hist.empty:
            date_string = (pd.to_datetime(df_stock_hist.loc[0].date) + pd.to_timedelta('1 days')).strftime('%Y-%m-%d')
        else:
            date_string = default_start_date

        print('index is ', stock_code, 'cur is ', cur_num, 'total ', total_num)
        cur_num = cur_num + 1

        rs = bs.query_history_k_data_plus(add_stock_code_prefix(stock_code),
                                          "date,time,code,open,high,low,close,volume",
                                          start_date=date_string,
                                          frequency=ktype_val, adjustflag="2")
        if len(rs.data) == 0:
            print('no new data for', stock_code)
            continue

        df_from_network = create_df_from_bao_rs_min(rs)


        if df_from_network is None:
            print('discard idle data')
            continue

        if not df_stock_hist.empty:
            df_stock_hist.set_index(['date', 'time'], inplace=True)
            df_from_network = mylib3.ma_update(df_stock_hist.head(20).copy(), df_from_network)
            df_stock_joined = pd.concat([df_from_network, df_stock_hist])
            df_stock_joined.to_csv(hist_file)
        else:
            df_from_network = mylib3.ma(df_from_network)
            df_from_network = mylib3.boll(df_from_network)
            df_from_network.to_csv(hist_file)

        #pdb.set_trace()

def add_ma_boll(df):
    df = df.loc[df['volume'] != 0]
    df = mylib3.ma(df)
    return mylib3.boll(df)

def add_boll(df):
    df = df.loc[df['volume'] != 0]
    return mylib3.boll(df)

def add_rsi(df):
    df = df.loc[df['volume'] != 0]
    return mylib3.rsi(df)

def reset_columns(df):
    #first, rename columns with corret names.
    df.columns = ['open', 'high', 'low', 'close', 'volume', 'turn', 'p_change']

    #secondly, put 'close' before 'open'
    columns = ['close', 'open', 'high', 'low', 'volume', 'turn', 'p_change']
    df_new = df.reindex(columns=columns)
    return df_new

def drop_zero_volume(df):
    df = df.loc[df['volume'] != 0]
    return df

if __name__ == "__main__":
    tick_dir = Path().joinpath('..', '..', 'stockdata-bao')
    load_history(tick_dir, 'basic-no3.csv', 'd')
    #load_history_min(tick_dir, 'basic-no3.csv')
    #load_history_min(tick_dir, 'basic-no3.csv', ktype_val='15')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', add_boll, 'w')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', reset_columns, 'd')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', drop_zero_volume, 'd')
    #load_history(tick_dir, 'basic-no3.csv', 'w')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', add_ma_boll, '60')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', add_ma, '60')