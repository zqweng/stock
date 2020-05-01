
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator

import matplotlib.animation as animation
from itertools import count
from matplotlib import style
from threading import Thread
import queue
import socket
import pdb

plt.rcParams['font.sans-serif'] = ['SimHei']

local_ip    = "127.0.0.1"
udp_buffer_size = 10240

# this class contain two callback functions, one is called for animation, another is called by Threading object as work function
class AnimationThread(Thread):
    def __init__(self, bind_port = 20001, grid_row_num= 10, axspan = 2):
        Thread.__init__(self)
        self.fig = plt.figure()
        self.colspan = axspan
        self.rowspan = axspan
        self.gridRowNum = grid_row_num
        self.gridColNum = grid_row_num
        self.axArray = []

        for i in range(self.gridRowNum // self.rowspan):
            for j in range(self.gridColNum // self.colspan):
                ax = plt.subplot2grid(
                    (self.gridRowNum, self.gridColNum),
                    (i * self.rowspan, j * self.colspan), colspan=self.colspan, rowspan=self.rowspan)
                #ax.autoscale(enable=False, axis='x')
                line, = ax.plot(0, 0)
                y_data = []
                x_data = []
                self.axArray.append((line, ax, y_data, x_data))

        self.df = pd.DataFrame()
        self.anim_return = animation.FuncAnimation(self.fig, func=self.animate, interval=10000)

        self.socket_buffer_size = 10240
        self.local_port = bind_port
        self.socket_server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket_server.bind((local_ip, self.local_port))

    def animate(self, i):
        # self.df have data received from UPD socket
        if self.df.empty:
            return

        #enumerate return a iterable object, in a "for in" statement, the method next() of this object is called implicitly
        for idx, pl in enumerate(self.axArray):

            # number of axes to draw upon must not exceed num of stock
            if idx >= len(self.df.index):
                break

            price = self.df.loc[idx].price

            #pl[3] and pl[2] are x y lists for a specified ax that are stored in axArray
            pl[3].append(i)
            pl[2].append(price)

            #pl[1] is a axe, we set subtitle and font size and color
            pl[1].set_xlim(0, i + 50)
            pl[1].set_ylim(price * 0.98, price * 1.02)
            #fontsize: {size in points, 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
            change = self.df.loc[idx].p_change
            pl[1].title.set_text('{} {}'.format(self.df.loc[idx][0], round(change, 2)))
            pl[1].title.set_size('medium')
            if change > 0:
                pl[1].title.set_color('red')
            else:
                pl[1].title.set_color('black')

            pl[0].set_xdata(pl[3])
            pl[0].set_ydata(pl[2])

    def run(self):
        while (True):
            receive_tuple = self.socket_server.recvfrom(self.socket_buffer_size)
            message = receive_tuple[0]
            address = receive_tuple[1]

            #message received from UDP is in Jason
            #https://medium.com/better-programming/strings-unicode-and-bytes-in-python-3-everything-you-always-wanted-to-know-27dc02ff2686
            clientMsg = message
            df = pd.read_json(clientMsg, orient='index', dtype='object')
            df.pre_close = df.pre_close.astype("float32")
            df.price = df.price.astype("float32")
            clientIP = "Client IP Address:{}".format(address)
            del self.df
            self.df = df


if __name__ == "__main__":
    obj = AnimationThread(20001)
    #obj2 = AnimationThread(20002)
    obj.start()
    #obj2.start()
    plt.show()
    obj.join()
