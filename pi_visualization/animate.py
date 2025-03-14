import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def animate_pi_spiral(pi_digits):
    """Animate the digits of Pi into a spiral pattern."""
    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro')

    def init():
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        return ln,

    def update(frame):
        angle = frame * 0.1
        radius = int(pi_digits[frame % len(pi_digits)]) / 10
        xdata.append(radius * np.cos(angle))
        ydata.append(radius * np.sin(angle))
        ln.set_data(xdata, ydata)
        return ln,

    ani = FuncAnimation(fig, update, frames=range(1000), init_func=init, blit=True)
    plt.show()
