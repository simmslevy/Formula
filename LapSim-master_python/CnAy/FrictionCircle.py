import matplotlib.pyplot as plt
import numpy as np


def plot_circle(tire_max_lat_g, tire_max_long_g, engine_limited_max_accel):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.plot([-tire_max_lat_g, tire_max_lat_g], [engine_limited_max_accel, engine_limited_max_accel],
            color='r',
            label='Power limited acceleration')

    trange = np.linspace(-np.pi, np.pi, endpoint=True, num=100)
    ax.plot(tire_max_lat_g * np.cos(trange), tire_max_long_g * np.sin(trange), color='b')
    plt.title('Friction Circle', fontsize=20)
    plt.ylabel(r'Max $A_{long}$ [g]', fontsize=20)
    plt.xlabel(r'Max $A_{lat}$ [g]', fontsize=20)
    plt.grid(True)
    plt.legend()
    plt.show()


plot_circle(1.36, 1.1, 0.5)