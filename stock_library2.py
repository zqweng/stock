import datetime
import os
import pandas as pd
from pathlib import Path
import pdb

head_offset = 0

def find_price_up_for_n_period(df, name,  code, latest_n_days, result_list, para1, para2):
    price_up_num = 0
    for i in range(latest_n_days):
        if df.loc[i].p_change <= 0:
            if price_up_num >= para1:
                result_list.append(tuple((name, code, df.loc[i - 1].date,
                                          df.loc[i - price_up_num - 1].date,
                                          price_up_num,0)))
                return
            else:
                price_up_num = 0
        else:
            price_up_num = price_up_num + 1

    if price_up_num >= para1:
        result_list.append(tuple((name, code, df.loc[i - 1].date,
                                  df.loc[i - price_up_num - 1].date,
                                  price_up_num, 0)))
        
    return True

def find_ma5_up(df, name,  code, latest_n_days, result_list, para1, para2):
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

"check if price of type para1 go up from last day for latest_n_periods"
def is_price_go_up_for_n_period(df, latest_n_periods, para1, para2):
    for i in range(latest_n_periods):
        if para1 == 'close':
            if df.loc[i].p_change <= 0:
                return False
        if para1 == 'ma5':
            if df.loc[i].ma5 <= df.loc[i+1].ma5:
                return False
        elif para1 == 'ma10':
            if df.loc[i].ma10 <= df.loc[i + 1].ma10:
                return False
        elif para1 == 'ma20':
            if df.loc[i].ma20 <= df.loc[i + 1].ma20:
                return False

    return True

def get_price(df, i, para):
    if para == 'close':
        return df.loc[i].close
    elif para == 'ma5':
        return df.loc[i].ma5
    elif para == 'ma10':
        return df.loc[i].ma10
    elif para == 'ma20':
        return df.loc[i].ma20
    else:
        return None

"check if para1 type of price is always above para2 type of price for the same day for latest_n_periods"

def is_price_above(df, latest_n_periods, para1, para2):
    for i in range(latest_n_periods):
        price1 = get_price(df, i, para1)
        if price1 is None:
            print('wrong para1')
            return None
        price2 = get_price(df, i, para2)
        if price2 is None:
            print('wrong para2')
            return None
        if price1 <= price2:
            return False

    return True

def find_cross_ma20(df, name,  code, latest_n_days, result_list, para1, para2):
    down_cross_ma20 = False
    up_cross_ma20 = False
    ma5_below_ma20 = False
    end_index = 0
    start_index = 0
    for i in range(latest_n_days):
        if not up_cross_ma20:
            if df.loc[i].close > df.loc[i].ma20 and df.loc[i + 1].close <= df.loc[i + 1].ma20:
                up_cross_ma20 = True
                end_index = i
        else:
            """
            ma5 must be above ma20 when price drops
            """
            if df.loc[i].close <= df.loc[i].ma20 and df.loc[i + 1].close > df.loc[i + 1].ma20:
                if df.loc[i].ma5 <= df.loc[i].ma20:
                    ma5_below_ma20 = True
                down_cross_ma20 = True
                start_index = i
                break

    if not ma5_below_ma20 and down_cross_ma20 and up_cross_ma20 and start_index - end_index >= para1 and \
            (start_index - end_index) <= para2:
        result_list.append(tuple((name, code, df.loc[end_index].date,
                                  df.loc[start_index].date,
                                  latest_n_days, 0)))
    return True

def find_price_go_up_for_n_period(df, name,  code, latest_n_days, result_list, para1, para2):
    cur_price = 0
    last_price = 0

    for i in range(latest_n_days):
        if para1 == 'ma5':
            cur_price = df.loc[i].ma5
            last_price = df.loc[i+1].ma5
        elif para1 == 'ma10':
            cur_price = df.loc[i].ma10
            last_price = df.loc[i+1].ma10
        elif para1 == 'ma20':
            cur_price = df.loc[i].ma20
            last_price = df.loc[i+1].ma20

        if para1 != 'p_change':
            if cur_price <= last_price:
                return
        else:
            if df.loc[i].p_change <= 0:
                return

    result_list.append(tuple((name, code, df.loc[0].date, df.loc[latest_n_days - 1].date,
                               latest_n_days, 0)))
    return True


def sum_of_latest_n_days_price_up(df, name,  code, latest_n_days, result_list, para1, para2):
    result_list.append(tuple((name, code, df.loc[0].date,
                              df.loc[latest_n_days-1].date,
                              latest_n_days, df[0:latest_n_days]['p_change'].sum())))
    return



def hist_callback(df, hist_dir, latest_n_days, callback, para1, para2, min_period=0):
    """
    current criteria is
    find up period list

    :param stock_list_file:
    :param df: dataframe includes the stock list to be analyzed
    :param hist_dir: stock history files for the stock list
    :param latest_n_days:
    :return: a new dataframe that meet the criteria.
    """

    start_time = datetime.datetime.now().time()
    stock_num = 0
    result_list = []

    for stock_row in df.itertuples():
        stock_code = stock_row.Index
        print('index is ', stock_code, 'num of stock is ', stock_num)
        stock_num = stock_num + 1

        if stock_code == '600161':
            continue

        csv_file = stock_code + '.csv'
        if not os.path.exists(os.path.join(hist_dir, csv_file)):
            print('file', csv_file, 'does not exist, skip it')
            continue

        stock_df = pd.read_csv(os.path.join(hist_dir, csv_file))

        if len(stock_df.index) < min_period:
            print('less than min period, discard it ', len(stock_df.index))
            continue

        if stock_df is None:
            print('failed to get history file ', stock_code)
            continue

        if latest_n_days == 0:
            frame_size = len(stock_df.index)
        else:
            frame_size = latest_n_days + 1

        #print('frame_size ', frame_size)
        if head_offset > 0:
            stock_df = stock_df[head_offset:]
            stock_df.reset_index(drop=True, inplace=True)

        callback(stock_df.head(frame_size), stock_row.name, stock_code, latest_n_days, result_list, para1, para2)

    #result_df = pd.DataFrame(result_list, columns=['name', 'code', 'start_date', 'end_date', 'days', 'p_change'])
    #result_df.code = result_df.code.astype('str')

    print(start_time)
    print(datetime.datetime.now().time())
    return result_list

"""
if __name__ == '__main__':
    result_string = ''
    tick_dir = Path().joinpath('..', '..', 'stockdata','week')
    # load_history(tick_dir, 'basic-no3.csv')
    result_df = hist_callback('basic-no3.csv', tick_dir, 5, find_ma5_up, 0, 0, 20)
    if not result_df.empty:
        result_string = result_string + "\n\nin last n days  ma5 up \n" + result_df.to_string()
    else:
        result_string = result_string + '\n\nno stock in last n days  has ma5 up \n'
    print(result_string)
"""
if __name__ == '__main__':
    stock_list_file = 'basic-no3.csv'
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    if df.empty:
        print('no stock list, quit')
        quit()
    result_string = ''
    result_string2 = ''
    tick_dir = Path().joinpath('..', '..', 'stockdata','day')
    # load_history(tick_dir, 'basic-no3.csv')
    min_number_of_days_below_ma20 = 2
    max_number_of_days_below_ma20 = 4
    result_df = hist_callback(df, tick_dir, 12, find_cross_ma20,
                              min_number_of_days_below_ma20,
                              max_number_of_days_below_ma20,
                              20)
    if not result_df.empty:
        result_string = result_string + "\n\nin last n days  ma5 up \n" + result_df.to_string()
    else:
        result_string = result_string + '\n\nno stock in last n days  has ma5 up \n'
    #print(result_string)

    tick_dir = Path().joinpath('..', '..', 'stockdata', 'week')
    result_df = hist_callback(result_df, tick_dir, 5, find_ma10_up,
                              0,
                              0,
                              20)

    if not result_df.empty:
        result_string2 = result_string + "\n\nin last n days  ma5 up \n" + result_df.to_string()
    else:
        result_string2 = result_string + '\n\nno stock in last n days  has ma5 up \n'
    #print(result_string2)