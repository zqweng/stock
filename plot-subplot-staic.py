
import matplotlib as mpl
#mpl.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator
from mpl_finance import candlestick2_ohlc

#mpl.use('TkAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']
fig = plt.figure()

colspan = 3
rowspan = 3
gridRowNum = 12
gridColNum = 12

numAxs = (gridColNum//colspan)*(gridRowNum//rowspan)
#axArray =[None] * numAxs
axArray = []
for i in range(gridRowNum//rowspan):
    for j in range(gridColNum//colspan):
        ax = plt.subplot2grid((gridRowNum, gridColNum), (i * rowspan, j * colspan), colspan=colspan, rowspan=rowspan)
        axArray.append(ax)


file_name = "/home/johnny/stockdata-bao/day/600004.csv"
df = pd.read_csv(file_name, nrows=200)
df = df.iloc[::-1]

#for ax in axArray:
#    ax.plot(df["open"])
#ax_vol = plt.subplot2grid((10, 10), (8, 0), colspan=10)
fig.subplots_adjust(bottom=0.2)
fig.set_size_inches(10, 8)

plt.show()