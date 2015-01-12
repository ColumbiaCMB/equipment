import time
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from equipment.Lake_Shore import gaussmeter

gm = gaussmeter.Gaussmeter425('/dev/tty.SLAB_USBtoUART')

length = 100
data = deque(np.zeros(length), maxlen=length)
t0 = time.time()
t = deque(np.zeros(length), maxlen=length)
fig, ax = plt.subplots(figsize=(3, 3))
ax.set_ylim(-1, 1)
(line,) = ax.plot(t, data, '-')

def append_gaussmeter_data():
    while True:
        t.append(time.time() - t0)
        data.append(gm.field)
        yield (t, data)

def append_random_data():
    while True:
        t.append(time.time()) - t0
        data.append(np.random.randn())
        yield (t, data)

def animate((t, data)):
    padding = 0.1 * (max(data) - min(data))
    ax.set_ylim(min(data) - padding, max(data) + padding)
    ax.set_xlim(min(t), max(t))
    line.set_xdata(t)
    line.set_ydata(data)
    return (ax, line)

anim = animation.FuncAnimation(fig, animate, frames=append_gaussmeter_data, interval=10)

plt.show()
