def check_point1(df, name,  code, latest_n_periods, result_list, para1, para2):

    if not is_price_up(df, latest_n_periods, 'ma5', 'ma10'):
        return False

    if not is_price_go_up(df, latest_n_periods, 'ma5', 'None'):
        return False

    if not is_price_go_up(df, latest_n_periods, 'ma10', 'None'):
        return False

    result_list.append(tuple((name, code, df.loc[end_index].date,
                              df.loc[start_index].date,
                              latest_n_days, 0)))

    return True


def check_point():
    stock_list_file = 'basic-no3.csv'
    df = pd.read_csv(Path().joinpath(stock_list_file), converters={'code': lambda x: str(x)})
    if df.empty:
        print('no stock list, quit')
        quit()
    result_string = ''

    tick_dir = Path().joinpath('..', '..', 'stockdata', 'day')
    result_df = hist_callback(result_df, tick_dir, 5, check_point1,
                              0,
                              0,
                              20)

    if not result_df.empty:
        result_string2 = result_string + "\n\n meet checkpoint 1 \n" + result_df.to_string()
    else:
        result_string2 = result_string + '\n\n no meet checkpoint 1\n'
    print(result_string2)