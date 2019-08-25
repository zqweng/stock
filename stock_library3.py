"""
basically we focus on

This library defines the weights of stock selection.

"""
import pdb

def macd(df):
    df.sort_index(ascending=True, inplace=True)
    macd12 = df['close'].ewm(span=12, adjust=False).mean()
    macd26 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = macd12 - macd26
    df['EXP3'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_HIST'] = df['MACD'] - df['EXP3']
    df.sort_index(ascending=False, inplace=True)
    return df


