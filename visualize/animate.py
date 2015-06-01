import time
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


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


def get_random():
    t0 = time.time()
    while True:
        t = time.time() - t0
        r = np.random.randn()
        yield t, r


def main():
    frame_delay_ms = 10  # in ms
    length = 128  # the number of samples displayed
    data = deque([], maxlen=length)
    times = deque([], maxlen=length)
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_xlabel('time [s]')
    ax.set_ylabel('random data [arbs]')
    line, = ax.plot(times, data, '-r')
    anim = animation.FuncAnimation(fig, animate, frames=get_random, fargs=(times, data, ax, line),
                                   interval=frame_delay_ms)
    plt.show()


if __name__ == '__main__':
    main()

