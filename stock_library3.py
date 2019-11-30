"""
basically we focus on

This library defines the weights of stock selection.

"""
import pdb
import pandas as pd
from talib.abstract import *


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
    df_old.sort_index(ascending=True, inplace=True)
    df_new.sort_index(ascending=True, inplace=True)

    df_new['ma5'] = 0
    df_new['ma10'] = 0
    df_new['ma20'] = 0
    df_new['upper'] = 0
    df_new['middle'] = 0
    df_new['lower'] = 0
    df_new = df_new.astype({'open': 'float64', 'high': 'float64', 'close': 'float64', 'low': 'float64', 'volume': 'int64'})
    df_concat = pd.concat([df_old, df_new])
    df_concat['ma5'] = df_concat['close'].rolling(5).mean()
    df_concat['ma10'] = df_concat['close'].rolling(10).mean()
    df_concat['ma20'] = df_concat['close'].rolling(20).mean()

    inputs = {
        'open': df_concat.open.values,
        'high': df_concat.high.values,
        'low': df_concat.low.values,
        'close': df_concat.close.values,
        'volume': df_concat.volume.values
    }

    df_concat['upper'], df_concat['middle'], df_concat['lower'] = BBANDS(inputs, 20, 2, 2)
    df_concat = df_concat.round(3)

    df_result = df_concat[-len(df_new.index):]
    return df_result.sort_index(ascending=False)

"""
   df_old should be a piece of dataframe with 20 rows used for calculate ma for new dataframe.
   after calculate we return the new piece. 
"""


def ma(df):
    df = df.sort_index(ascending=True)
    df['ma5'] = df['close'].rolling(5).mean()
    df['ma10'] = df['close'].rolling(10).mean()
    df['ma20'] = df['close'].rolling(20).mean()
    return df.sort_index(ascending=False)

def boll(df):
    df = df.sort_index(ascending=True)
    inputs = {
        'open': df.open.values,
        'high': df.high.values,
        'low': df.low.values,
        'close': df.close.values,
        'volume': df.volume.values
    }

    df['upper'], df['middle'], df['lower'] = BBANDS(inputs, 20, 2, 2)
    df = df.round(3)
    return df.sort_index(ascending=False)


def rsi(df):
    df = df.sort_index(ascending=True)
    close = df['close']
    delta = close.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    """
    roll_up1 = up.ewm(span=6, adjust=False).mean()
    roll_down1 = down.abs().ewm(span=6, adjust=False).mean()
    """
    roll_up2 = up.ewm(span=12, adjust=False).mean()
    roll_down2 = down.abs().ewm(span=12, adjust=False).mean()

    roll_up3 = up.ewm(span=24, adjust=False).mean()
    roll_down3 = down.abs().ewm(span=24, adjust=False).mean()

    roll_up1 = up.rolling(6).mean()
    roll_down1 = down.abs().rolling(6).mean()

    # Calculate the RSI based on EWMA
    rsi1 = roll_up1 / roll_down1
    df['rsi1'] = 100.0 - (100.0 / (1.0 + rsi1))

    # Calculate the RSI based on EWMA
    rsi2 = roll_up2 / roll_down2
    df['rsi2'] = 100.0 - (100.0 / (1.0 + rsi2))

    # Calculate the RSI based on EWMA
    rsi3 = roll_up3 / roll_down3
    df['rsi3'] = 100.0 - (100.0 / (1.0 + rsi3))

    return df.sort_index(ascending=False)
