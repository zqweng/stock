"""
basically we focus on

This library defines the weights of stock selection.

"""
import pdb
import pandas as pd


def macd(df):
    df.sort_index(ascending=True, inplace=True)
    macd12 = df['close'].ewm(span=12, adjust=False).mean()
    macd26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = macd12 - macd26
    df['EXP3'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_HIST'] = df['MACD'] - df['EXP3']
    df.sort_index(ascending=False, inplace=True)
    return df


"""
   df_old should be a piece of dataframe with 20 rows used for calculate ma for new dataframe.
   after calculate we return the new piece. 
"""


def ma_update(df_old, df_new):
    df_new['ma5'] = 0
    df_new['ma10'] = 0
    df_new['ma20'] = 0
    df_concat = pd.concat([df_old, df_new])
    df_concat['ma5'] = df_concat['close'].rolling(5).mean()
    df_concat['ma10'] = df_concat['close'].rolling(10).mean()
    df_concat['ma20'] = df_concat['close'].rolling(20).mean()
    return df_concat[-len(df_new.index):]


"""
   df_old should be a piece of dataframe with 20 rows used for calculate ma for new dataframe.
   after calculate we return the new piece. 
"""


def ma(df):
    df.sort_index(ascending=True, inplace=True)
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    df.sort_index(ascending=False, inplace=True)
    return df
