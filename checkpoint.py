import pandas as pd
import stock_library2 as mylib2
from pathlib import Path


def check_point_one_for_day(df, name,  code, latest_n_periods, result_list, para1, para2):

    ret = mylib2.is_price_above(df, latest_n_periods, 'ma5', 'ma10')
    if ret is None or not ret :
        return False

    ret = mylib2.is_price_above(df, latest_n_periods, 'ma10', 'ma20')
    if ret is None or not ret:
        return False

    if not mylib2.is_price_go_up_for_n_period(df, latest_n_periods, 'ma5', 'None'):
        return False

    if not mylib2.is_price_go_up_for_n_period(df, latest_n_periods, 'ma10', 'None'):
        return False

    if not mylib2.is_price_go_up_for_n_period(df, latest_n_periods, 'ma20', 'None'):
        return False

    result_list.append(tuple((name, code, '', '',
                              latest_n_periods, 0)))

    return True

def check_point_one_for_week(df, name,  code, latest_n_periods, result_list, para1, para2):

    if not mylib2.is_price_go_up_for_n_period(df, latest_n_periods, 'ma10', 'None'):
        return False

    if not mylib2.is_price_go_up_for_n_period(df, latest_n_periods, 'close', 'None'):
        return False
    result_list.append(tuple((name, code, '', '',
                              latest_n_periods, 0)))

    return True


def check_point():
    stock_list_file = 'basic-no3.csv'
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    if df.empty:
        print('no stock list, quit')
        quit()

    result_string = ''
    tick_dir = Path().joinpath('..', '..', 'stockdata', 'day')
    result_df = mylib2.hist_callback(df, tick_dir, 5, check_point_one_for_day,
                              0,
                              0,
                              20)

    if not result_df.empty:
        result_string2 = result_string + "\n\n meet checkpoint 1 \n" + result_df.to_string()
    else:
        result_string2 = result_string + '\n\n no meet checkpoint 1\n'
    #print(result_string2)

    tick_dir_week = Path().joinpath('..', '..', 'stockdata', 'week')
    result_df2 = mylib2.hist_callback(df, tick_dir_week, 3, check_point_one_for_week,
                                     0,
                                     0,
                                     20)

    if not result_df2.empty:
        result_df2 = result_df[result_df['code'].isin(result_df2['code'])]
        result_string2 = "\n\n meet checkpoint 1 \n" + result_df2.to_string()
    else:
        result_string2 = '\n\n no week meet checkpoint 1\n'
    print(result_string2)


if __name__ == '__main__':
    check_point()