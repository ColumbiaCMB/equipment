import time
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from equipment.Lake_Shore import gaussmeter

gm = gaussmeter.Gaussmeter425('/dev/tty.SLAB_USBtoUART')

length = 100
data = deque([0], maxlen=length)
times = deque([0], maxlen=length)
fig, ax = plt.subplots(figsize=(3, 3))
ax.set_xlabel('time [s]')
ax.set_ylabel('field [{}]'.format(gm.field_units))
(line,) = ax.plot(times, data, '-r')

def get_gaussmeter():
    t0 = time.time()
    while True:
        t = time.time() - t0
        f = gm.field
        yield t, f

def get_random():
    t0 = time.time()
    while True:
        t = time.time() - t0
        r = np.random.randn()
        yield t, r

def animate(framedata):
    t, y = framedata
    times.append(t)
    data.append(y)
    ax.set_xlim(min(times), max(times))
    padding = 0.1 * (max(data) - min(data)) or 1
    ax.set_ylim(min(data) - padding, max(data) + padding)
    line.set_xdata(times)
    line.set_ydata(data)
    return ax, line

anim = animation.FuncAnimation(fig, animate, get_gaussmeter, interval=1)
#anim = animation.FuncAnimation(fig, animate, frames=get_random, interval=100)

plt.show()
