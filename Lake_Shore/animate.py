import time
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from equipment.Lake_Shore import gaussmeter


def get_random():
    t0 = time.time()
    while True:
        t = time.time() - t0
        r = np.random.randn()
        yield t, r


def animate(framedata, times, data, ax, line):
    t, y = framedata
    times.append(t)
    data.append(y)
    t_padding = 0.1
    ax.set_xlim(times[0] - t_padding, times[-1] + t_padding)
    y_padding = 0.1 * (max(data) - min(data)) or 1
    ax.set_ylim(min(data) - y_padding, max(data) + y_padding)
    line.set_xdata(times)
    line.set_ydata(data)
    return ax, line

if __name__ == '__main__':
    gm = gaussmeter.Gaussmeter425('/dev/tty.SLAB_USBtoUART')

    # It's fine to use a 10 ms delay after sending and a 1 ms delay between frames because the gaussmeter slows down
    # communication to about 30 Hz; see the code.
    gm.communication_delay = gm.short_communication_delay
    frame_delay = 1  # in ms

    def get_gaussmeter():
        t0 = time.time()
        while True:
            t = time.time() - t0
            f = gm.field
            yield t, f

    length = 128
    data = deque([], maxlen=length)
    times = deque([], maxlen=length)
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_xlabel('time [s]')
    ax.set_ylabel('field [{}]'.format(gm.field_units))
    line, = ax.plot(times, data, '-r')

    anim = animation.FuncAnimation(fig, animate, frames=get_gaussmeter, fargs=(times, data, ax, line), interval=frame_delay)
    #anim = animation.FuncAnimation(fig, animate, frames=get_random, fargs=(times, data, ax, line), interval=100)

    plt.show()
