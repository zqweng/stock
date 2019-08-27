
import pandas as pd
from pathlib import Path
import tushare as ts
import stock_library3 as mylib3
import os


# hist_dir = '/home/johnny/python/csv/'
# stock_list_file = 'mystocklist-detail.csv'

def load_history(hist_dir, stock_list_file, ktype_val='D'):
    default_start_date = ''
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})
        index = df['code']
    if ktype_val == 'D' or ktype_val == 'd':
        hist_dir = os.path.join(hist_dir, 'day')
    elif ktype_val == 'W' or ktype_val == 'w':
        hist_dir = os.path.join(hist_dir, 'week')
    if not os.path.exists(hist_dir):
        os.mkdir(hist_dir)
    #os.chdir(hist_dir)

    total_num = len(index)
    cur_num = 1
    date_string = ''

    for stock_code in index:
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

        df_from_network = ts.get_h_data(stock_code, start=date_string, ktype=ktype_val)
        if df_from_network is None:
            print('fail get history file', stock_code)
            continue
        if df_from_network.empty:
            print('no new data for', stock_code)
            continue

        if not df_stock_hist.empty:
            df_stock_hist.set_index('date', inplace=True)

        df_stock_joined = pd.concat([df_from_network, df_stock_hist])

        df_stock_joined = mylib3.macd(df_stock_joined)

        df_stock_joined.to_csv(hist_file)



def add_history_with_MACD(hist_dir, stock_list_file, ktype_val='D'):
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})
        index = df['code']

    if ktype_val == 'D' or ktype_val == 'd':
        new_hist_dir = os.path.join(hist_dir, 'macdday')
        hist_dir = os.path.join(hist_dir, 'day')
    elif ktype_val == 'W' or ktype_val == 'w':
        new_hist_dir = os.path.join(hist_dir, 'macdweek')
        hist_dir = os.path.join(hist_dir, 'week')

    if not os.path.exists(new_hist_dir):
        os.mkdir(new_hist_dir)

    total_num = len(index)
    cur_num = 1
    date_string = ''

    for stock_code in index:
        hist_file = os.path.join(hist_dir, stock_code + '.csv')
        new_hist_file = os.path.join(new_hist_dir, stock_code + '.csv')

        if os.path.isfile(hist_file):
            df_stock_hist = pd.read_csv(hist_file)
        else:
            continue

        print('index is ', stock_code, 'cur is ', cur_num, 'total ', total_num)
        cur_num = cur_num + 1

        df_stock_hist.set_index('date', inplace=True)
        df_stock_joined = mylib3.macd(df_stock_hist)
        df_stock_joined.to_csv(new_hist_file)

def remove_item_with_the_date(hist_dir, stock_list_file, ktype_val='W'):
    if not os.path.isfile(stock_list_file):
        print('股票清单 not exist, create one')
        quit()
    else:
        print('股票清单 exists, load it')
        df = pd.read_csv(stock_list_file, converters={'code': lambda x: str(x)})

    if ktype_val == 'D' or ktype_val == 'd':
        hist_dir = os.path.join(hist_dir, 'day')
    elif ktype_val == 'W' or ktype_val == 'w':
        hist_dir = os.path.join(hist_dir, 'week')

    cur_num = 1
    date_string = ''

    for stock_code in df['code']:
        hist_file = os.path.join(hist_dir, stock_code + '.csv')

        if os.path.isfile(hist_file):
            df_stock_hist = pd.read_csv(hist_file)
        else:
            continue

        print('index is ', stock_code, 'cur is ', cur_num, 'total ', df.count)
        cur_num = cur_num + 1
        df_stock_hist[1:].to_csv(hist_file)

def recalculate_ma10(df):
    df['ma10'] = df['ma5'] + df['ma5'].shift(-5)

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

    if not os.path.exists(new_hist_dir):
        os.mkdir(new_hist_dir)

    total_num = len(index)
    cur_num = 1
    date_string = ''

    for stock_code in index:
        hist_file = os.path.join(hist_dir, stock_code + '.csv')
        new_hist_file = os.path.join(new_hist_dir, stock_code + '.csv')

        if os.path.isfile(hist_file):
            df_stock_hist = pd.read_csv(hist_file)
        else:
            continue

        print('index is ', stock_code, 'cur is ', cur_num, 'total ', total_num)
        cur_num = cur_num + 1

        callback(df_stock_hist)
        df_stock_hist.to_csv(new_hist_file)


if __name__ == "__main__":
    tick_dir = Path().joinpath('..', '..', 'stockdata')
    #'mystocklist-detail.csv'
    #load_history(tick_dir, 'mystocklist-detail.csv')
    #add_history_with_MACD(tick_dir, 'basic-no3.csv')
    load_history(tick_dir, 'basic-no3.csv', 'W')
    #update_history_with_callback(tick_dir, 'basic-no3.csv', recalculate_ma10, )