
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick2_ohlc

mpl.use('TkAgg')

def draw_k_lines(quotes):
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    fig.set_size_inches(15, 15)
    candlestick2_ohlc(ax, quotes['open'], quotes['high'], quotes['low'], quotes['close'], width=0.5)
    plt.show()
