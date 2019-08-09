"""v3, add a chinese stock name to output file
       set encoding='ansi' for the output csv file 
"""

"""Pandas dtype	Python type	NumPy type	Usage
   object	str	string_, unicode_	Text
   int64	int	int_, int8, int16, int32, int64, uint8, uint16, uint32, uint64	Integer numbers
   float64	float	float_, float16, float32, float64	Floating point numbers
   bool	bool	bool_	True/False values
   datetime64	NA	datetime64[ns]	Date and time values
   timedelta[ns]	NA	NA	Differences between two datetimes
   category	NA	NA	Finite list of text values
"""

"""
using a dic to define a row, and create a dataframe using an array of dic 
row1 = {'a':5,'b':6,'c':7,'d':'A'}
row2 = {'a':8,'b':9,'c':10,'d':'B'}
row3 = {'a':11,'b':12,'c':13,'d':'C'}
df = pd.DataFrame([row1,row2,row3])
"""

import datetime
import os
import pandas as pd
import pdb


def day_lower_shadow_line(row):
    if row.open >= row.close:
        return 0

    if row.open == row.low:
        return 0

    if (row.close - row.low) / row.close < 0.04:
        return 0

    shadow_ratio = (row.open - row.low) / (row.close - row.open)

    #if shadow_ratio > 2:
    #shade_list.append(tuple((shade_ratio, stock_row.name, row.date, stock_code)))
    print(' ratio:', shadow_ratio, ' date:', row.date, ' open:', row.open, ' close:',
          row.close, ' low:', row.low, ' ma5', row.ma5, ' ma10', row.ma10, ' ma20:',
          row.ma20)
    return shadow_ratio
          
def day_break_moving_avg(row):
    if row.ma5 > row.ma10 or row.p_change < 2:
        return

    close_above = False
    open_below = False
    low_below = False
    date_val = row.date

    if row.close > row.ma5 and \
            row.close > row.ma10 and \
            row.close > row.ma20:
        close_above = True

    if row.open < row.ma5 and \
            row.open < row.ma10 and \
            row.open < row.ma20:
        open_below = True

    if row.low < row.ma5 and \
            row.low < row.ma10 and \
            row.low < row.ma20:
        low_below = True

    if close_above and (open_below or low_below):
        print('date:', date_val, ' open:', row.open,
              ' close:', row.close, ' low:', row.low, ' ma5', row.ma5, ' ma10',
              row.ma10, ' ma20:', row.ma20)
        return True

    return False


def day_price_calculate(df, hist_dir, latest_n_days, name):
    start_time = datetime.datetime.now().time()
    stock_num = 0
    result_list = []

    for stock_row in df.itertuples():
        stock_code = stock_row.code
        print('index is ', stock_code, 'num of stock is ', stock_num)
        stock_num = stock_num + 1

        csv_file = stock_code + '.csv'
        if not os.path.exists(hist_dir + csv_file):
            print('file', csv_file, 'does not exist, skip it')
            continue

        stock_df = pd.read_csv(hist_dir + csv_file, nrows=latest_n_days + 1)

        if stock_df is None:
            print('failed to get history file ', stock_code)
            continue

        row_num = 0

        # read each tick data for each date in that history table

        for row in stock_df.itertuples():
            if name == 'break ma':
                if day_break_moving_avg(row):
                    result_list.append(tuple((stock_row.name, row.date, stock_code)))
            elif name == 'lower shadow':
                ratio = day_lower_shadow_line(row)
                if ratio >= 2:
                    result_list.append(tuple((stock_row.name, row.date, stock_code)))
                    

    result_df = pd.DataFrame(result_list, columns=['name', 'date', 'code'])
    result_df.code = result_df.code.astype('str')

    print(start_time)
    print(datetime.datetime.now().time())
    return result_df


def day_k_cross(df, hist_dir, latest_n_days):
    """
    current criteria is
    ma5 cross m10
    ma5 rise
    ma5 is above ma20

    :param df: dataframe includes the stock list to be analyzed
    :param hist_dir: stock history files for the stock list
    :param latest_n_days:
    :return: a new dataframe that meet the criteria.
    """
    start_time = datetime.datetime.now().time()
    stock_num = 0
    result_list = []

    for stock_row in df.itertuples():
        stock_code = stock_row.code
        print('index is ', stock_code, 'num of stock is ', stock_num)
        stock_num = stock_num + 1

        csv_file = stock_code + '.csv'
        if not os.path.exists(hist_dir + csv_file):
            print('file', csv_file, 'does not exist, skip it')
            continue

        stock_df = pd.read_csv(hist_dir + csv_file, nrows=latest_n_days + 1)

        if stock_df is None:
            print('failed to get history file ', stock_code)
            continue

        row_num = 0

        # read each tick data for each date in that history table

        # for row in stock_df.itertuples():
        for i in range(0, latest_n_days):
            # print('code ', stock_code, 'date ', row.date)
            if stock_df.loc[i].ma5 > stock_df.loc[i].ma10 and \
                    stock_df.loc[i + 1].ma5 <= stock_df.loc[i + 1].ma10 and \
                    stock_df.loc[i].ma5 > stock_df.loc[i + 1].ma5 and \
                    stock_df.loc[i].ma5 > stock_df.loc[i].ma20:
                print('code ', stock_code, 'date ', stock_df.loc[i].date)
                result_list.append(tuple((stock_row.name, stock_df.loc[i].date, stock_code)))

    result_df = pd.DataFrame(result_list, columns=['name', 'date', 'code'])
    result_df.code = result_df.code.astype('str')

    print(start_time)
    print(datetime.datetime.now().time())
    return result_df
