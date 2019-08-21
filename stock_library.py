"""
   v3, add a chinese stock name to output file
       set encoding='ansi' for the output csv file 

   Pandas dtype	Python type	NumPy type	Usage
   object	str	string_, unicode_	Text
   int64	int	int_, int8, int16, int32, int64, uint8, uint16, uint32, uint64	Integer numbers
   float64	float	float_, float16, float32, float64	Floating point numbers
   bool	bool	bool_	True/False values
   datetime64	NA	datetime64[ns]	Date and time values
   timedelta[ns]	NA	NA	Differences between two datetimes
   category	NA	NA	Finite list of text values

    using a dic to define a row, and create a dataframe using an array of dic
    row1 = {'a':5,'b':6,'c':7,'d':'A'}
    row2 = {'a':8,'b':9,'c':10,'d':'B'}
    row3 = {'a':11,'b':12,'c':13,'d':'C'}
    df = pd.DataFrame([row1,row2,row3])

    when you write a library, the external symbols used by the library code needs to be imported first.
    For example, the main python file imports pandas library and it calls the function which needs pandas in this library and it will
    still fails if this library does not import pandas itself.
"""
import datetime
import os
import pandas as pd
import pdb


def resampl_by_hour(tick_df, resample_intv, date_val):
    tick_df['time'] = date_val + ' ' + tick_df['time']
    tick_df['time'] = pd.to_datetime(tick_df['time'])
    tick_df = tick_df.set_index('time')

    loffset_val = '30min'
    new_tick_df = tick_df['price'].resample(resample_intv, loffset=loffset_val).ohlc()
    new_tick_df = new_tick_df.dropna()
    vols = tick_df['volume'].resample(resample_intv, loffset=loffset_val).sum()
    vols = vols.dropna()
    vol_df = pd.DataFrame(vols, columns=['volume'])
    amounts = tick_df['amount'].resample(resample_intv, loffset=loffset_val).sum()
    amounts = amounts.dropna()
    amount_df = pd.DataFrame(amounts, columns=['amount'])
    newdf = new_tick_df.merge(vol_df, left_index=True,
                              right_index=True).merge(amount_df,
                                                      left_index=True,
                                                      right_index=True)
    new_file_name = date_val + '-' + resample_intv + '.csv'
    # newdf.to_csv(new_file_name)
    if newdf is None:
        print('create resample df fail ', date_val, 'for stock', stock_code)
        return None
    else:
        # print('successfully created a file ', new_file_name)
        return newdf


def resample_local(tick_df, resample_intv, date_val, loffset_val='0min'):
    new_tick_df = tick_df['price'].resample(resample_intv, loffset=loffset_val).ohlc()
    new_tick_df = new_tick_df.dropna()
    vols = tick_df['volume'].resample(resample_intv, loffset=loffset_val).sum()
    vols = vols.dropna()
    vol_df = pd.DataFrame(vols, columns=['volume'])
    amounts = tick_df['amount'].resample(resample_intv, loffset=loffset_val).sum()
    amounts = amounts.dropna()
    amount_df = pd.DataFrame(amounts, columns=['amount'])
    newdf = new_tick_df.merge(vol_df, left_index=True,
                              right_index=True).merge(amount_df,
                                                      left_index=True,
                                                      right_index=True)
    new_file_name = date_val + '-' + resample_intv + '.csv'
    # newdf.to_csv(new_file_name)
    if newdf is None:
        print('create resample df fail ', date_val, 'for stock', stock_code)
        return None
    else:
        # print('successfully created a file ', new_file_name)
        return newdf


def resample(tick_df, resample_intv, date_val):
    tick_df['time'] = date_val + ' ' + tick_df['time']
    tick_df['time'] = pd.to_datetime(tick_df['time'])
    tick_df = tick_df.set_index('time')

    if resample_intv == '60min':
        startTime = tick_df.index[0]
        tick_df_morning = tick_df[(tick_df.index - startTime).seconds < 10000]
        tick_df_morning = resample_local(tick_df_morning, resample_intv, date_val, '30min')
        tick_df_afternoon = tick_df[(tick_df.index - startTime).seconds >= 10000]
        tick_df_afternoon = resample_local(tick_df_afternoon, resample_intv, date_val)
        return pd.concat([tick_df_morning, tick_df_afternoon])

    else:
        return resample_local(tick_df, resample_intv, date_val)


def day_lower_shadow_line(row):
    if row.open >= row.close:
        return 0

    if row.open == row.low:
        return 0

    if (row.close - row.low) / row.close < 0.04:
        return 0

    shadow_ratio = (row.open - row.low) / (row.close - row.open)

    # if shadow_ratio > 2:
    # shade_list.append(tuple((shade_ratio, stock_row.name, row.date, stock_code)))
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
        if not os.path.exists(os.path.join(hist_dir, csv_file)):
            print('file', csv_file, 'does not exist, skip it')
            continue

        stock_df = pd.read_csv(os.path.join(hist_dir, csv_file), nrows=latest_n_days + 1)

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
        if not os.path.exists(os.path.join(hist_dir, csv_file)):
            print('file', csv_file, 'does not exist, skip it')
            continue

        stock_df = pd.read_csv(os.path.join(hist_dir, csv_file), nrows=latest_n_days + 1)

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

def is_higher_shadow_line(row):
    return (row.high - row.close) > (row.close - row.open)

def is_small_up(row):
    return 1 <= row.p_change < 4 and not is_higher_shadow_line(row)

def day_n_days_small_up(df, hist_dir, num_of_up, latest_n_days):
    """
    find the stock that continually rise during n days between [1% - 4%)
    """
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

        stock_df = pd.read_csv(os.path.join(hist_dir, csv_file), nrows=latest_n_days + 3)

        if stock_df is None:
            print('failed to get history file ', stock_code)
            continue

        row_num = 0

        # read each tick data for each date in that history table

        # for row in stock_df.itertuples():
        for i in range(0, latest_n_days):
            # print('code ', stock_code, 'date ', row.date)
            if is_small_up(stock_df.loc[i]) and \
                    is_small_up(stock_df.loc[i+1]) and \
                    is_small_up(stock_df.loc[i+2]):
                print('code ', stock_code, 'date ', stock_df.loc[i].date)
                result_list.append(tuple((stock_row.name, stock_df.loc[i].date, stock_code)))
                break

    result_df = pd.DataFrame(result_list, columns=['name', 'date', 'code'])
    result_df.code = result_df.code.astype('str')

    print(start_time)
    print(datetime.datetime.now().time())
    return result_df

def day_find_up_period(df, stock_code, result_list):
    """
    find the up period by checking ma5. up period must meet the following conditions:
    1: the close price of the second bottom of rise period must be higher than the bottom one. otherwise, start all
       over again.
    2: ma5 price must always rise up. else
    3: if ma5 drop for the first time, the price of that day must be 15% higher than the bottom price.otherwise,
       start all over again.
    4:if ma5 drop continue 4 days in a row, period end.
    :param df:
    :return:
    """
    rise_bottom = -1
    rise_ceil = -1
    ma5_down = 0
    #pdb.set_trace()
    for i in df.index:
        if i == 0:
            """
            first item must be the bottom
            """
            rise_bottom = 0
        else:
            if rise_bottom == -1:
                print('new bottom ma5', i, df.loc[i].date)
                if df.loc[i].ma5 > df.loc[i-1].ma5:
                    rise_bottom = i - 1
                    rise_ceil = i
                    ma5_down = 0
            else:
                print ('i=', i, ' ma5=', df.loc[i].ma5)
                if df.loc[i].ma5 >= df.loc[i-1].ma5:
                    rise_ceil = i
                    ma5_down = 0
                    print('continue bottom ma5', df.loc[rise_bottom].ma5 )
                else:
                    """
                    first time ma5 drop could only happen after ma5 rise no less than 13%,
                    otherwise it is not an up period
                    """
                    if ma5_down == 0:
                        ma5_down = 1
                        if (df.loc[i].ma5 - df.loc[rise_bottom].ma5)/df.loc[rise_bottom].ma5 < 0.1:
                            print('reset bottom ma5', df.loc[rise_bottom].ma5, 'current ma5 ', df.loc[i].ma5)
                            rise_bottom = -1
                            rise_ceil = -1
                        else:
                            print('first time ma5 down, but since it rise up to 10%, lets continue')
                    else:
                        ma5_down = ma5_down + 1
                        print ('ma5_down is ', ma5_down)
                        """
                        if ma5 drop 4 days in a row, rise terminate.
                        """
                        if ma5_down >= 4:
                            print('find one: start index ', rise_bottom, ' end index ', rise_ceil)
                            ma5_down = 0
                            result_list.append(tuple((stock_code, df.loc[rise_bottom].date, df.loc[rise_ceil].date,
                                                      rise_ceil - rise_bottom + 1,
                                                      (df.loc[rise_ceil].ma5 - df.loc[rise_bottom].ma5)*100
                                                      /df.loc[rise_bottom].ma5)))
                            rise_bottom = -1
                            rise_ceil = -1

    if rise_ceil != -1 and rise_bottom != -1:
        if (df.loc[i].ma5 - df.loc[rise_bottom].ma5) / df.loc[
            rise_bottom].ma5 >= 0.1:
            result_list.append(tuple((stock_code, df.loc[rise_bottom].date,
                                      df.loc[rise_ceil].date, rise_ceil - rise_bottom + 1,
                                      (df.loc[rise_ceil].ma5 - df.loc[rise_bottom].ma5) * 100
                                      /df.loc[rise_bottom].ma5)))


def day_find_up_period_list(df, hist_dir, latest_n_days):
    """
    current criteria is
    find up period list

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
        if not os.path.exists(os.path.join(hist_dir, csv_file)):
            print('file', csv_file, 'does not exist, skip it')
            continue

        stock_df = pd.read_csv(os.path.join(hist_dir, csv_file), nrows=latest_n_days + 1)

        if stock_df is None:
            print('failed to get history file ', stock_code)
            continue

        row_num = 0

        # read each tick data for each date in that history table
        if 'data' in stock_df.columns:
            stock_df.set_index('date', inplace=True)
        elif 'time' in stock_df.columns:
            stock_df.set_index('time', inplace=True)

        stock_df.sort_index(ascending=1, inplace=True)
        stock_df.reset_index(inplace=True)
        day_find_up_period(stock_df,stock_code, result_list)

    result_df = pd.DataFrame(result_list, columns=['code', 'start_date', 'end_date', 'days', 'p_change'])
    result_df.code = result_df.code.astype('str')

    print(start_time)
    print(datetime.datetime.now().time())
    return result_df

