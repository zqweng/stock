
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator

import matplotlib.animation as animation
from itertools import count
from matplotlib import style
import pdb
plt.rcParams['font.sans-serif'] = ['SimHei']

fig = plt.figure()

colspan = 6
rowspan = 6
gridRowNum = 12
gridColNum = 12

axArray = []

for i in range(gridRowNum//rowspan):
    for j in range(gridColNum//colspan):
        ax = plt.subplot2grid((gridRowNum, gridColNum), (i * rowspan, j * colspan), colspan=colspan, rowspan=rowspan)
        ax.autoscale(enable=False, axis='x')
        ax.set_xlim(0, 100)
        ax.set_ylim(10,20)
        axArray.append(ax)


file_name = "/home/johnny/stockdata-bao/day/600004.csv"
df = pd.read_csv(file_name, nrows=200)
#df = df.iloc[::-1]
iter = count(start=1)

def animate(i):
    df1 = df[:next(iter)]
    for ax in axArray:
        ax.clear()
        ax.plot(df1["open"])

#ax_vol = plt.subplot2grid((10, 10), (8, 0), colspan=10)
#fig.subplots_adjust(bottom=0.2)
#fig.set_size_inches(10, 8)
animation = animation.FuncAnimation(fig, func=animate, interval=1000)
plt.show()