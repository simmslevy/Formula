__author__ = 'gpearman'
import pylab
from multiprocessing import Pool
from functools import partial
import scipy.optimize


_colors = 'rgbcmyk'


def _get_y(x, points_func, goal):
    def to_optimize(y):
        return points_func(x, y) - goal

    try:
        return scipy.optimize.broyden1(to_optimize, [1], f_tol=0.1, maxiter=10)[0]
    except:
        print("Did not converge for x: {x} goal: {goal}".format(**locals()))
        return 0


def plot_colored_by_points(points_func, x_linspace, xlabel='', ylabel='', colored_by=(650,), pool_size=4):
    """
    Plot a graph with lines of constant value across two variables (x, y)
    :param points_func: a function that takes in x and y
    :param x_linspace: an iterable defining the points on the x axis
    :param xlabel: a label for the x axis
    :param ylabel: a label for the y axis
    :param colored_by: an iterable containing the goal for each line
    :param pool_size: number of cpu cores to use
    :return: nothing
    """
    partial_get_ys = {partial(_get_y, points_func=points_func, goal=colored): str(colored) for colored in colored_by}
    plot_many_y_funcs(partial_get_ys, x_linspace, xlabel=xlabel, ylabel=ylabel, pool_size=pool_size)


def plot_many_y_funcs(y_funcs, x_linspace, xlabel='', ylabel='Points', pool_size=4):
    """
    Plot many functions on one graph.
    :param y_funcs: a dictionary where each key is a function and each value is the label for that function.
    :param x_linspace: values for the x axis
    :param xlabel: label for the x axis
    :param ylabel: label for the y axis
    :param pool_size: number of cpu cores to use
    :return: nothing
    """
    color_index = -1

    def get_next_color():
        nonlocal color_index
        color_index += 1
        return _colors[color_index]

    pool = Pool(processes=pool_size)
    for y_func, y_func_label in y_funcs.items():
        points = pool.map(y_func, x_linspace)
        pylab.plot(x_linspace, points, get_next_color(), label=y_func_label)

    pylab.legend()
    pool.close()
    pylab.ylabel(ylabel, fontsize=20)
    pylab.xlabel(xlabel, fontsize=20)
    pylab.show()


def contour_plot(f, xlist, ylist, xlabel='', ylabel='', pool_size=4):
    """
    Plot a contour plot.
    :param f: The function to plot, should be a function that has x and y as parameters.
    :param xlist: x axis values of the plot, should be an iterable
    :param ylist: y axis values of the plot, should be an iterable
    :param xlabel: the x axis label
    :param ylabel: the y axis label
    :param pool_size: number of cpu cores to use
    :return: nothing
    """
    pool = Pool(processes=pool_size)

    z = []
    for x in xlist:
        z.append([])
        partial_f = partial(f, x=x)
        z[-1] = pool.map(partial_f, ylist)

    pool.close()

    cs = pylab.contour(xlist, ylist, z, [725, 750, 775, 800, 825], linewidths=[1], colors='b')
    pylab.clabel(cs, inline=1, fontsize=10)
    pylab.ylabel(ylabel, fontsize=20)
    pylab.xlabel(xlabel, fontsize=20)
    pylab.show()