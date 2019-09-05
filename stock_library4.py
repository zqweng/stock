import pandas as pd
import os
from pathlib import Path
import pdb
def find_w_shape(df, name,  code, latest_n_days, result_list, para1, para2):
    """
    the original index was int, we change it to date and sort it in ascending order
    :param df:
    :param name:
    :param code:
    :param latest_n_days:
    :param result_list:
    :param para1:
    :param para2:
    :return:
    """
    df.set_index('date', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    print('find w shape for ', code, ' starting ', df.index[0])

    lowest_index = df[['low']].idxmin()
    lowest_price = df[['low']].min()
    df_after_lowest = df[df.index > lowest_index.low]


    first_rise_percentage = 0
    first_peek_index = None
    first_peek_price = 0

    for row in df_after_lowest.itertuples():
        """
        first rising period must be steep and no drop close
        """
        if row.p_change <= 0:
            if first_rise_percentage <= 15:
                first_peek_index = None
            break
        else:
            first_rise_percentage = first_rise_percentage + row.p_change
            first_peek_index = row.Index
            first_peek_price = row.high

    if first_peek_index is None:
        return

    if df.loc[lowest_index.low].ma5 > df.loc[lowest_index.low].ma10:
        return

    if df.loc[lowest_index.low].ma10 > df.loc[lowest_index.low].ma20:
        return

    df_after_peek = df_after_lowest[df_after_lowest.index > first_peek_index]
    if df_after_peek.empty:
        return

    second_lowest_index = df_after_peek[['low']].idxmin()
    second_lowest_price = df_after_peek[['low']].min()
    if (first_peek_price - second_lowest_price.low) / second_lowest_price.low <= 0.15:
        return

    df_peek_to_low = df_after_peek[df_after_peek.index < second_lowest_index.low]
    if first_peek_price < df_peek_to_low[['high']].max().high:
        return

    if len(df_peek_to_low.index) > 10:
        return

    result_list.append(tuple((name, code, first_peek_index, second_lowest_index.low, latest_n_days, lowest_index.low)))
    return


def find_history_high(df, name,  code, latest_n_days, result_list, para1, para2):
    """
    the original index was int, we change it to date and sort it in ascending order
    :param df:
    :param name:
    :param code:
    :param latest_n_days:
    :param result_list:
    :param para1: within number of days, price break record
    :param para2: record type, could be all time, one year, etc.
    :return:
    """

    #print('find history record for ', code)

    history_dir = Path().joinpath('..', '..', 'stockdata-bao', 'month')
    df_history = pd.read_csv((os.path.join(history_dir, code + '.csv')))
    if df_history is None:
        print("month file for ", code, " does not exist")
        return
    """
    don't count the recent month
    """
    df_history = df_history[:-1]
    if para2 > 0:
        df_history = df_history.tail(para2)

    for row in df.head(latest_n_days).itertuples():
        lower = False
        for row_history in df_history.itertuples():
            #print ('price ', row.high, ' and month high is ', row_history.high)
            if row.high <= row_history.high:
                lower = True
                break
        if not lower:
            result_list.append(tuple((name, code, row.date, 0, 0, latest_n_days)))
            return


def find_price_up_and_no_touch_ma5_for_n_period(df, name, code, latest_n_days, result_list, para1, para2):
    price_up_num = 0
    for i in range(latest_n_days):
        boolean = 4 > df.loc[i].p_change > 0 and df.loc[i].ma5 < df.loc[i].low \
                  and df.loc[i].low > df.loc[i+1].low
        if not boolean:
            if price_up_num >= 2:
                result_list.append(tuple((name, code, df.loc[i - 1].date,
                                          df.loc[i - price_up_num].date,
                                          price_up_num, 0)))
                return
            else:
                price_up_num = 0
        else:
            price_up_num = price_up_num + 1

    if price_up_num >= 2:
        result_list.append(tuple((name, code, df.loc[i - 1].date,
                                  df.loc[i - price_up_num - 1].date,
                                  price_up_num, 0)))

    return True
