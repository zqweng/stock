import pandas as pd
import random
from mpl_finance import candlestick2_ohlc
import pdb

class StockSample():
    def __init__(self, ax):

        code = "002152"
        self.df = pd.read_csv("/home/johnny/stockdata-bao/day/{}.csv".format(code), nrows=300)
        self.max_record = self.df.shape[0]
        self.df = self.df.iloc[::-1]
        self.df = self.df.reset_index()
        self.counter = 0
        self.display_num = 150

        end_index = random.randint(0 , len(self.df.index))

        df_slice = self.df[0: self.display_num]

        self.plot(ax, df_slice)

    def plot_next(self,ax):

        if self.counter + self.display_num < self.max_record:
            self.counter += 1

        df_slice = self.df[self.counter: self.display_num + self.counter]
        df_slice = df_slice.reset_index()

        self.plot(ax,df_slice)

    def plot_prev(self,ax):

        self.counter -= 1 if self.counter > 0 else 0

        df_slice = self.df[self.counter: self.display_num + self.counter]
        df_slice = df_slice.reset_index()

        self.plot(ax,df_slice)

    def plot(self, ax, df_slice):

        candlestick2_ohlc(ax[0], df_slice['open'], df_slice['high'], df_slice['low'], df_slice['close'],
                          width=0.6, colorup='r', colordown='k',)
        ax[0].plot(df_slice["ma5"], "k", label="ma5", linewidth=0.5)
        ax[0].plot(df_slice["ma10"], "y", label="ma10", linewidth=0.5)
        ax[0].plot(df_slice["ma20"], "r", label="ma20", linewidth=0.5)
        ax[0].plot(df_slice["upper"], "b--", label="upper", linewidth=0.5)
        ax[0].plot(df_slice["lower"], "b--", label="upper", linewidth=0.5)
        text = df_slice.tail(1).p_change.values[0]
        ax[0].set_title("price change {}".format(str(text)))

        color = ""
        for x in df_slice['p_change']:
            if x >= 0:
                color += 'r'
            else:
                color += 'k'

        ax[1].bar(df_slice.index, df_slice["volume"], color = color)





