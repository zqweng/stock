
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator

import matplotlib.animation as animation
from itertools import count
from matplotlib import style
from threading import Thread
import queue

plt.rcParams['font.sans-serif'] = ['SimHei']

plt_show_on = False

class AnimationThread(Thread):
    def __init__(self, queue = None, grid_row_num= 10, colspan = 2):
        Thread.__init__(self)
        self.fig = plt.figure()
        self.colspan = colspan
        self.rowspan = colspan
        self.gridRowNum = grid_row_num
        self.gridColNum = grid_row_num
        self.axArray = []
        self.y_data = []
        self.x_data = []
        self.queue = queue
        for i in range(self.gridRowNum // self.rowspan):
            for j in range(self.gridColNum // colspan):
                ax = plt.subplot2grid(
                    (self.gridRowNum, self.gridColNum),
                    (i * self.rowspan, j * self.colspan), colspan=self.colspan, rowspan=self.rowspan)
                ax.autoscale(enable=False, axis='x')
                ax.set_ylim(10,20)
                line, = ax.plot(0, 0)
                self.axArray.append((line, ax))
        file_name = "/home/johnny/stockdata-bao/day/600004.csv"
        self.df = pd.read_csv(file_name, nrows=200)
        self.anim_return = animation.FuncAnimation(self.fig, func=self.animate, interval=10000)
        #df = df.iloc[::-1]

    def animate(self, i):
        self.x_data.append(i)
        self.y_data.append(self.df.loc[i].open)
        for pl in self.axArray:
            pl[1].set_xlim(0, i + 50)
            pl[0].set_xdata(self.x_data)
            pl[0].set_ydata(self.y_data)

    def run(self):
        item = self.queue.get()
        global plt_show_on
        if not plt_show_on:
            plt_show_on = True
            plt.show()


#ax_vol = plt.subplot2grid((10, 10), (8, 0), colspan=10)
#fig.subplots_adjust(bottom=0.2)
#fig.set_size_inches(10, 8)

if __name__ == "__main__":
    q1 = queue.Queue()
    obj = AnimationThread(q1)
    q2 = queue.Queue()
    obj2 = AnimationThread(q2)
    obj.start()
    obj2.start()
    plt.show()
    obj.join()
