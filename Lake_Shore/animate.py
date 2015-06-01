import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib import animation
from equipment.visualize import animate
from equipment.Lake_Shore import gaussmeter

# TODO: add command line options
if __name__ == '__main__':
    gm = gaussmeter.Gaussmeter425('/dev/tty.SLAB_USBtoUART')

    def get_gaussmeter():
        t0 = time.time()
        while True:
            t = time.time() - t0
            f = gm.field
            yield t, f

    # It's fine to use a 10 ms delay after sending and a 1 ms delay between frames because the gaussmeter slows down
    # communication to about 30 Hz; see the code.
    gm.communication_delay = gm.short_communication_delay
    frame_delay = 1  # in ms

    length = 128
    data = deque([], maxlen=length)
    times = deque([], maxlen=length)
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_xlabel('time [s]')
    ax.set_ylabel('field [{}]'.format(gm.field_units))
    line, = ax.plot(times, data, '-r')
    anim = animation.FuncAnimation(fig, animate, frames=get_gaussmeter, fargs=(times, data, ax, line),
                                   interval=frame_delay)
    plt.show()
