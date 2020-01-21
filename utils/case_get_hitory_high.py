import os
import pandas as pd
import api as myapi
from pathlib import Path
import pdb

def get_one_year_high():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_one_year_high.csv')

    # stock_list_file = 'mystocklist-detail.csv'
    df = myapi.read_csv(stock_list_file)
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_history_high(df, 10, 12)
    df_result.to_csv(tmpfile)

def get_history_high_v2():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_history_high_v2.csv')
    df = myapi.read_csv(stock_list_file)
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_history_high_v2(df, 10)
    df_result.to_csv(tmpfile)

def get_one_year_high_v2():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_one_year_high_v2.csv')
    df = myapi.read_csv(stock_list_file)
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_history_high_v2(df, 5, 250)
    df_result.to_csv(tmpfile)

def get_half_year_high_v2():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_half_year_high_v2.csv')
    df = myapi.read_csv(stock_list_file)
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_history_high_v2(df, 3, 120)
    df_result.to_csv(tmpfile)

def get_history_high_volume():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_history_high_volume.csv')
    df = myapi.read_csv(stock_list_file)
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_history_high_volume(df, 10)
    df_result.to_csv(tmpfile)

def get_one_year_high_volume():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_one_year_high_volume.csv')
    df = myapi.read_csv(stock_list_file)
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_history_high_volume(df, 2, 250)
    df_result.to_csv(tmpfile)

def get_first_history_high_volume_in_10_days():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_first_history_high_volume_in_10_days.csv')
    df = myapi.read_csv(stock_list_file)
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_first_history_high_volume_in_n(df, 2)
    df_result.to_csv(tmpfile)

def get_first_one_year_high_volume_in_10_days():
    stock_list_file = 'basic-no3.csv'
    tmpfile = Path().joinpath('result', 'get_first_one_year_high_volume_in_10_days.csv')
    df = myapi.read_csv(stock_list_file)
    df = myapi.remove_unwanted_fields(df)

    """
    in latest 10 days, find history high
    """
    df_result = myapi.get_first_history_high_volume_in_n(df, 2, 250)
    df_result.to_csv(tmpfile)
    return df_result