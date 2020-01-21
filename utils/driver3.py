"""
when you import
"""
import pandas as pd
from utils import stock_library as mylib
from pathlib import Path

# pdb.set_trace()

stock_list_file = 'mystocklist-detail.csv'

# stock_list_file = 'test_list.csv'

def test_find_up_period_in_days():
    history_dir = Path().joinpath('..', '..', 'stockdata', 'day')
    # update_history.load_history(history_dir, stock_list_file)

    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})

    if df.empty:
        print('no stock list, quit')

    result_df3 = mylib.day_find_up_period_list(df, history_dir, 120)
    if not result_df3.empty:
        result_string = result_string + '\n\nprice has 3 days up between 1% and 4% \n' + result_df3.to_string()
    else:
        result_string = result_string + '\n\nno price has 3 days up between 1% and 4% \n'
    print(result_string)


def test_find_up_period(type, period):
    result_string = ''
    history_dir = Path().joinpath('..', '..', 'stockdata', type)
    # update_history.load_history(history_dir, stock_list_file)

    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})

    if df.empty:
        print('no stock list, quit')

    result_df3 = mylib.day_find_up_period_list(df, history_dir, period)
    if not result_df3.empty:
        result_string = result_string + '\n\nprice has 3 days up between 1% and 4% \n' + result_df3.to_string()
    else:
        result_string = result_string + '\n\nno price has 3 days up between 1% and 4% \n'
    print(result_string)

if __name__ == '__main__':
    #test_find_up_period('day', 120)
    test_find_up_period('60min', 120)

