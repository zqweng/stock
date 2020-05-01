from matplotlib import pyplot as plt
from matplotlib import animation
import pandas as pd
import pdb

f0 = pd.DataFrame({'firstColumn': [1,2,3,4,5], 'secondColumn': [1,2,3,4,5]})
f1 = pd.DataFrame({'firstColumn': [5,4,3,2,1], 'secondColumn': [1,2,3,4,5]})
f2 = pd.DataFrame({'firstColumn': [5,4,3.5,2,1], 'secondColumn': [5,4,3,2,1]})

# make a global variable to store dataframes
global mylist
mylist=[f0,f1,f2]

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 5), ylim=(0, 5))
line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function of dataframes' list
def animate(i):

    line.set_data(mylist[i]['firstColumn'], mylist[i]['secondColumn'])
    return line,

# call the animator, animate every 300 ms
# set number of frames to the length of your list of dataframes
anim = animation.FuncAnimation(fig, animate, frames=len(mylist), init_func=init, interval=300, blit=True)

plt.show()