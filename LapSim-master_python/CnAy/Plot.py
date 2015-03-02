import sys
from multiprocessing import Pool
from Constants import *
import matplotlib.pyplot as plt
from TrigHelpers import *
from functools import partial
from scipy.integrate import quad
from scipy import interpolate, optimize
from scipy.misc import derivative
from time import strftime
from utils import ensure_dir
import json
from CnAy.SteeringFunctions import SteeringFunction


def _get_slip_angle(turn_center_x, turn_center_y, tire_x, tire_y, static_angle, plot=False):
    if turn_center_x < tire_x:
        alpha = (sign(tire_y - turn_center_y)
                 * abs(degrees(angle_between((1, 0), (tire_x - turn_center_x, tire_y - turn_center_y))))
                 - static_angle)
    else:
        alpha = (sign(tire_y - turn_center_y)
                 * abs(degrees(angle_between((1, 0), (tire_x - turn_center_x, tire_y - turn_center_y))))
                 + 180 - static_angle)
    if alpha > 180:
        alpha -= 360
    elif alpha < -180:
        alpha += 360

    if plot:
        plt.plot([tire_x], [tire_y], 'ro')
        plt.plot([tire_x, tire_x - sind(alpha)], [tire_y, tire_y + cosd(alpha)], 'r')
        plt.plot([tire_x, tire_x - sind(static_angle)], [tire_y, tire_y + cosd(static_angle)], 'g')
        plt.plot([tire_x, turn_center_x], [tire_y, turn_center_y], 'c')  # plot beta to turn center

    return alpha


def get_cn_ay(a_y, b, a_x, steer_func, steer_wheel_angle, toe_in_front, toe_in_rear, percent_rear_weight, wheelbase,
              track_front, track_rear, tire_func, cg_height, weight_lbs, v_nom, lltd, debug=False, **kwargs):
    """
    Determine an (ay, cn) point for the AyCn graph.

    This function takes in the car parameters, including a beta and steering angle, and tries to optimize the output.
    Since this function both takes in ay as an input and returns ay as an output, this function must be called many
    times until the input and output ay are the same.

    :param b: the car slip angle (degrees)
    :param a_y: the car's latitudinal acceleration (g)
    :param a_x: the car's longitudinal acceleration (g)
    :param steer_func: a subclass of CnAy.SteeringFunctions.SteeringFunction
    :param steer_wheel_angle: the steering wheel angle, measured at the steering wheel (degrees)
    :param toe_in_front: static angle of the front tires, positive is towards the center of the car (degrees)
    :param toe_in_rear: static angle of the rear tires, positive is towards the center of the car (degrees)
    :param percent_rear_weight: 0.0 <= percent_rear_weight <= 1.0, percent_rear_weight = rear_weight / total_weight
    :param wheelbase: longitudinal distance from front tire center axis to rear tire center axis (meters)
    :param track_front: distance between the centers of the front tires (meters)
    :param track_rear: distance between the centers of the rear tires (meters)
    :param tire_func: a function that takes in alpha and load and returns fy (function)
    :param cg_height: height of the car cg, measured from the ground (meters)
    :param weight_lbs: total weight of the car (lbs)
    :param v_nom: corner speed (m/s)
    :param lltd: 0.0 <= lltd <= 1.0, lltd = front_load_transfer / total_load_transfer
    :return: (ay, cn)
    """
    if percent_rear_weight > 1.0 or percent_rear_weight < 0.0:
        raise ValueError("percent_rear_weight must be between 0 and 1")
    if lltd > 1.0 or lltd < 0.0:
        raise ValueError("LLTD must be between 0 and 1")
    if wheelbase <= 0.0:
        raise ValueError("Wheelbase must be positive")
    if track_front <= 0.0:
        raise ValueError("track_front must be positive")
    if track_rear <= 0.0:
        raise ValueError("track_rear must be positive")
    if not isinstance(steer_func, SteeringFunction):
        raise TypeError("steer_func must be an instance of the SteeringFunction class")

    cg_to_front = wheelbase * percent_rear_weight
    cg_to_rear = wheelbase - cg_to_front

    # R is in m
    if a_y == 0.0:
        r = sys.maxsize
    else:
        r = v_nom ** 2.0 / (a_y * g)

    # deltas
    delta_fl = steer_func.get_fl(steer_wheel_angle)
    delta_fr = steer_func.get_fr(steer_wheel_angle)
    delta_rl = steer_func.get_rl(steer_wheel_angle)
    delta_rr = steer_func.get_rr(steer_wheel_angle)

    # slip angles
    if debug:
        fig = plt.figure()
        plot = fig.add_subplot(111, aspect='equal')
        plt.plot([-r * cosd(b)], [-r * sind(b)], 'bo')
        plt.plot([0], [0], 'go')  # cg
        plt.plot([0, -sind(b)], [0, cosd(b)], 'r')  # plot beta
        plt.plot([0, -r * cosd(b)], [0, -r * sind(b)], 'c')  # plot beta to turn center

    # FL slip angle
    alpha_fl = _get_slip_angle(turn_center_x=-r * cosd(b),
                               turn_center_y=-r * sind(b),
                               tire_x=-track_front / 2.0,
                               tire_y=cg_to_front,
                               static_angle=delta_fl - toe_in_front,
                               plot=debug)

    # FR slip angle
    alpha_fr = _get_slip_angle(turn_center_x=-r * cosd(b),
                               turn_center_y=-r * sind(b),
                               tire_x=track_front / 2.0,
                               tire_y=cg_to_front,
                               static_angle=delta_fr + toe_in_front,
                               plot=debug)

    # RL slip angle
    alpha_rl = _get_slip_angle(turn_center_x=-r * cosd(b),
                               turn_center_y=-r * sind(b),
                               tire_x=-track_rear / 2.0,
                               tire_y=-cg_to_rear,
                               static_angle=delta_rl - toe_in_rear,
                               plot=debug)

    # RR slip angle
    alpha_rr = _get_slip_angle(turn_center_x=-r * cosd(b),
                               turn_center_y=-r * sind(b),
                               tire_x=track_rear / 2.0,
                               tire_y=-cg_to_rear,
                               static_angle=delta_rr + toe_in_rear,
                               plot=debug)

    if debug:
        print("# Slip angles\nFL: {alpha_fl}\nFR: {alpha_fr}\nRL: {alpha_rl}\nRR: {alpha_rr}\n".format(**locals()))

    # load on each tire (lbf)
    load_transfer_lat = cg_height / ((track_front + track_rear) / 2.0) * a_y * weight_lbs  # lbf
    load_transfer_lat_front = load_transfer_lat * lltd
    load_transfer_lat_rear = load_transfer_lat * (1.0 - lltd)

    load_transfer_long = cg_height / wheelbase * a_x * weight_lbs  # lbf

    load_front = weight_lbs * (1.0 - percent_rear_weight) - load_transfer_long
    load_rear = weight_lbs * percent_rear_weight + load_transfer_long
    load_fl = load_front / 2.0 - load_transfer_lat_front
    load_fr = load_front / 2.0 + load_transfer_lat_front
    load_rl = load_rear / 2.0 - load_transfer_lat_rear
    load_rr = load_rear / 2.0 + load_transfer_lat_rear

    # no load can be negative
    if load_fl < 0:
        load_fl = 0.0
        load_fr = load_front
    if load_fr < 0:
        load_fr = 0.0
        load_fl = load_front
    if load_rl < 0:
        load_rl = 0.0
        load_rr = load_rear
    if load_rr < 0:
        load_rr = 0.0
        load_rl = load_rear

    if debug:
        print("# Loads (lbf) \nFL: {load_fl}\nFR: {load_fr}\nRL: {load_rl}\nRR: {load_rr}\n".format(**locals()))

    # get Fy (lbf) for each tire
    tire_fy_fl = tire_func(alpha_fl, load_fl) if load_fl > 0.0 else 0.0
    tire_fy_fr = tire_func(alpha_fr, load_fr) if load_fr > 0.0 else 0.0
    tire_fy_rl = tire_func(alpha_rl, load_rl) if load_rl > 0.0 else 0.0
    tire_fy_rr = tire_func(alpha_rr, load_rr) if load_rr > 0.0 else 0.0

    # longitudinal force from tire slip (lbf, car frame)
    #Fy_car_frame = (abs(sind(delta_fl - toe_in_front)) * tire_fy_fl + abs(sind(delta_fr + toe_in_front)) * tire_fy_fr +
    #                abs(sind(delta_rl - toe_in_rear)) * tire_fy_rl + abs(sind(delta_rr + toe_in_rear)) * tire_fy_rr)

    if debug:
        print("# Forces\nFL: {tire_fy_fl}\nFR: {tire_fy_fr}\nRL: {tire_fy_rl}\nRR: {tire_fy_rr}\n".format(**locals()))

    # calculate yaw
    car_fy_front = tire_fy_fl * cosd(delta_fl - toe_in_front) + tire_fy_fr * cosd(delta_fr + toe_in_front)  # lbf
    car_fy_rear = tire_fy_rl * cosd(toe_in_rear) + tire_fy_rr * cosd(toe_in_rear)  # lbf

    # calculate cn
    cn = N_PER_LBF * (car_fy_front * cg_to_front - car_fy_rear * cg_to_rear) / (weight_lbs * N_PER_LBF) / wheelbase * -1.0

    # calculate ay
    a_y = (car_fy_front + car_fy_rear) * (N_PER_LBF / g) / (weight_lbs * N_PER_LBF / g) * -1.0

    if debug:
        plt.show()

    return a_y, cn


def get_cn_ay_point(partial_cn_ay_func):
    """
    Return the (Ay, Cn) point that satifies the partial function.
    :param partial_cn_ay_func: a functools.partial that takes in Ay and returns (Ay, Cn)
    :return: a tuple with the satisfying (Ay, Cn) point
    """
    def to_optimize(ay):
        return partial_cn_ay_func(ay)[0] - ay

    ay = optimize.broyden1(to_optimize, [1.5], verbose=False)[0]
    return partial_cn_ay_func(ay)


def make_plot(default_params,
              pool_size=4,
              constant_steer_angles=(-90, -60, -40, -20, -10, 0, 10, 20, 40, 60, 90),
              constant_beta_angles=(-16.0, -8.0, -2.0, -1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0, 2.0, 8, 16.0),
              **kwargs):
    """
    Make many Cn Ay plots using default_params for the defaults and kwargs for the sweep ranges.
    :param default_params: a dictionary containing the default parameters to use for the get_Cn_Ay function
    :param pool_size: number of threads to use. set equal to the number of cores your computer has for fastest results
    :param kwargs: kwargs come from keys of default_params. kwarg values should be np.linspaces and represent sweeps
    :return: nothing
    """
    for param in kwargs:
        if param not in default_params:
            raise KeyError("{param} is not a parameter get_Cn_Ay takes as input".format(param=param))
    folder = strftime("%Y.%m.%d %H.%M.%S")

    # start the threads
    pool = Pool(processes=pool_size)

    for param, linspace in kwargs.items():
        # start fresh each loop
        params = default_params.copy()

        param_values, areas, max_ays, max_trimmed_ays = [], [], [], []
        max_yaws, max_trimmed_yaws, stability_indexs, control_indexs = [], [], [], []
        for value in linspace:
            params[param] = value
            params['weight_lbs'] = params['car_lbs'] + params['driver_lbs']

            # initialize figure and plot
            fig = plt.figure()
            ax = fig.add_subplot(111)

            # draw constant beta lines
            beta_results = {}
            for beta in constant_beta_angles:
                params['b'] = beta

                # we create many functions to execute
                partial_funcs = []
                for steer_wheel_angle in np.linspace(-90, 90, 100):
                    params['steer_wheel_angle'] = steer_wheel_angle
                    partial_funcs.append(partial(get_cn_ay, **params))

                # we don't know how the pool will return our results so we sort the results by A_y values
                values = sorted(pool.map(get_cn_ay_point, partial_funcs), key=lambda x: x[0])
                ax.plot([A_y for (A_y, yaw) in values], [yaw for (A_y, yaw) in values], 'b')

                # depending on beta we label the line at the right or left side of the plot (for readability)
                if beta > 0:
                    ax.text(values[-1][0], values[-1][1], str(beta), size=8, color='b', ha="left", va="bottom")
                else:
                    ax.text(values[0][0], values[0][1], str(beta), size=8, color='b', ha="right", va="top")

                # keep the results for finding the control index later
                beta_results[beta] = values

            # iterate through constant steering wheel angles, comments from constant beta lines should explain this loop
            steer_wheel_angle_results = {}
            for steer_wheel_angle in constant_steer_angles:
                params['steer_wheel_angle'] = steer_wheel_angle

                partial_funcs = []
                # TODO is this the correct range
                betas = [x for x in range(-60, -8, 1)]
                betas += [x for x in np.linspace(-8.0, 8.0, endpoint=True, num=100)]
                betas += [x for x in range(8, 61, 1)]
                for beta in betas:
                    params['b'] = beta
                    partial_funcs.append(partial(get_cn_ay, **params))

                values = sorted(pool.map(get_cn_ay_point, partial_funcs), key=lambda x: x[0])
                ax.plot([A_y for (A_y, yaw) in values], [yaw for (A_y, yaw) in values], 'r')

                # TODO there must be a better way of doing these labels
                dist = 10
                for (A_y, yaw) in values:
                    if abs(A_y) < dist and 0.55 > yaw > -0.55:
                        dist = abs(A_y)
                        middle_x = A_y
                        middle_y = yaw
                ax.text(middle_x, middle_y, str(steer_wheel_angle),
                        size=8, color='r', ha="center", va="center", bbox={'ec': '1', 'fc': '1'})

                # keep the results for finding things like stability index later
                steer_wheel_angle_results[steer_wheel_angle] = values

            # find the max Ay and yaw
            max_ay = max([ay for _, results in steer_wheel_angle_results.items() for (ay, yaw) in results])
            max_yaw = max([yaw for _, results in steer_wheel_angle_results.items() for (ay, yaw) in results])

            # find the max trimmed Ay
            max_trimmed_ay = max(pool.map(partial(_get_max_trimmed_ay, max_ay=max_ay),
                                          steer_wheel_angle_results.values()))

            # find the max trimmed yaw
            interpolated = {}
            for angle, ay_yaw_list in steer_wheel_angle_results.items():
                interpolated[angle] = interpolate.interp1d([a_y for (a_y, yaw) in ay_yaw_list],
                                                           [yaw for (a_y, yaw) in ay_yaw_list],
                                                           kind='linear')

            max_trimmed_yaw = max(interpolated[angle](0.0) for angle in steer_wheel_angle_results)

            # get the area
            def interpolated_safe(interpolated, max_input, min_input, x):
                x = max_input if x > max_input else x
                x = min_input if x < min_input else x
                return interpolated(x)

            def integrand(x):
                values = []
                for angle, func in interpolated.items():
                    values.append(interpolated_safe(func, steer_wheel_angle_results[angle][-1][0],
                                                    steer_wheel_angle_results[angle][0][0], x))
                return max(values) - min(values)

            area = quad(integrand, -max_ay, max_ay)[0]

            # get the stability index
            interpolated = interpolate.interp1d([A_y for (A_y, yaw) in steer_wheel_angle_results[0.0]],
                                                [yaw for (A_y, yaw) in steer_wheel_angle_results[0.0]],
                                                kind='linear')

            def f(x):
                x = steer_wheel_angle_results[0.0][0][0] if x < steer_wheel_angle_results[0.0][0][0] else x
                x = steer_wheel_angle_results[0.0][-1][0] if x > steer_wheel_angle_results[0.0][-1][0] else x
                return interpolated(x)
            stability_index = derivative(f, 0.0)

            # get the control index
            interpolated = interpolate.interp1d([A_y for (A_y, yaw) in beta_results[0.0]],
                                                [yaw for (A_y, yaw) in beta_results[0.0]],
                                                kind='linear')

            def f(x):
                x = beta_results[0.0][0][0] if x < beta_results[0.0][0][0] else x
                x = beta_results[0.0][-1][0] if x > beta_results[0.0][-1][0] else x
                return interpolated(x)
            control_index = derivative(f, 0.0)

            # axis labels
            plt.ylabel(r'$C_N$ [unitless]', fontsize=20)
            plt.xlabel(r'$A_y$ [g]', fontsize=20)

            # axis range
            # TODO do plot limits automagically, look at trim lines
            plt.xlim([-1.7, 1.7])
            plt.ylim([-1.0, 1.0])

            # plot title
            plt.title('{0} - {1:0.3f}'.format(param, value), fontsize=20)

            # plot info
            info_box = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            info_str = 'Area: {area:0.4f}\n'.format(area=area)
            info_str += 'Max {ay_latex}: {max_ay:0.4f}\n'.format(max_ay=max_ay, ay_latex=r'$A_y$')
            info_str += 'Max Trimmed {ay_latex}: {max_trimmed_ay:0.4f}\n'.format(max_trimmed_ay=max_trimmed_ay,
                                                                                 ay_latex=r'$A_y$')
            info_str += 'Max Yaw: {max_yaw:0.4f}\n'.format(max_yaw=max_yaw)
            info_str += 'Max Trimmed Yaw: {max_trimmed_yaw:0.4f}\n'.format(max_trimmed_yaw=float(max_trimmed_yaw))
            info_str += 'Stability Index: {stability_index:0.4f}\n'.format(stability_index=stability_index)
            info_str += 'Control Index:  {control_index:0.4f}'.format(control_index=control_index)

            info_text = plt.figtext(0.93, 0.91, info_str, fontsize=14, verticalalignment='top', bbox=info_box)

            d = params.copy()
            d['tire_func'] = params['tire_func'].name
            d['steer_func'] = params['steer_func'].__class__.__name__
            param_str = json.dumps(d, indent=1)[2:-2]
            param_text = plt.figtext(0.93, 0.59, param_str, fontsize=14, verticalalignment='top', bbox=info_box)

            # make a legend, put it below the x axis
            ax.plot([], [], color='r', label='Constant Steering Angle')
            ax.plot([], [], color='b', label=r'Constant $\beta$')

            # dotted trim lines
            ax.plot([-1.7, 1.7], [0, 0], 'k--', alpha=0.3, label='Trim')
            ax.plot([0, 0], [-0.9, 0.9], 'k--', alpha=0.3)
            lgd = ax.legend(bbox_to_anchor=(0.5, -0.16), loc='upper center', borderaxespad=0., ncol=2)

            # save the figure
            savefolder = '../out/' + folder + '/{0}/'.format(param)
            ensure_dir(savefolder)
            fig.savefig(savefolder + '/{0} - {1:0.3f}.png'.format(param, value),
                        bbox_extra_artists=(lgd, info_text, param_text),
                        bbox_inches='tight')
            plt.close()

            param_values.append(value)
            areas.append(area)
            max_ays.append(max_ay)
            max_trimmed_ays.append(max_trimmed_ay)
            max_yaws.append(max_yaw)
            max_trimmed_yaws.append(max_trimmed_yaw)
            stability_indexs.append(stability_index)
            control_indexs.append(control_index)

        # overview plots
        # TODO make this prettier
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(param_values, max_ays, color='b')
        plt.title(r'{0} Sweep - Max $A_y$'.format(param), fontsize=20)
        plt.ylabel(r'Max $A_y$ [g]', fontsize=20)
        plt.xlabel('{0}'.format(param), fontsize=20)
        fig.savefig(savefolder + '{0} - Max Ay.png'.format(param), bbox_inches='tight')
        plt.close()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(param_values, areas, color='b')
        plt.title(r'{0} Sweep - $C_n$ $A_y$ Area'.format(param), fontsize=20)
        plt.title('{0} Sweep'.format(param), fontsize=20)
        plt.ylabel('Area [unitless * g]', fontsize=20)
        plt.xlabel('{0}'.format(param), fontsize=20)
        fig.savefig(savefolder + '{0} - Area.png'.format(param), bbox_inches='tight')
        plt.close()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(param_values, max_trimmed_ays, color='b')
        plt.title(r'{0} Sweep - Max Trimmed $A_y$'.format(param), fontsize=20)
        plt.ylabel(r'$A_y$ [g]', fontsize=20)
        plt.xlabel('{0}'.format(param), fontsize=20)
        fig.savefig(savefolder + '{0} - Max Trimmed Ay.png'.format(param), bbox_inches='tight')
        plt.close()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(param_values, max_yaws, color='b')
        plt.title(r'{0} Sweep - Max Yaw'.format(param), fontsize=20)
        plt.ylabel(r'$C_N$ [unitless]', fontsize=20)
        plt.xlabel('{0}'.format(param), fontsize=20)
        fig.savefig(savefolder + '{0} - Max Yaw.png'.format(param), bbox_inches='tight')
        plt.close()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(param_values, max_trimmed_yaws, color='b')
        plt.title(r'{0} Sweep - Max Trimmed Yaw'.format(param), fontsize=20)
        plt.ylabel(r'$C_N$ [unitless]', fontsize=20)
        plt.xlabel('{0}'.format(param), fontsize=20)
        fig.savefig(savefolder + '{0} - Max Trimmed Yaw.png'.format(param), bbox_inches='tight')
        plt.close()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(param_values, stability_indexs, color='b')
        plt.title(r'{0} Sweep - Stability Index'.format(param), fontsize=20)
        plt.ylabel(r'Stability Index [unitless / g]', fontsize=20)
        plt.xlabel('{0}'.format(param), fontsize=20)
        fig.savefig(savefolder + '{0} - Stability Index.png'.format(param), bbox_inches='tight')
        plt.close()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(param_values, control_indexs, color='b')
        plt.title(r'{0} Sweep - Control Index'.format(param), fontsize=20)
        plt.ylabel(r'Control Index [unitless / g]', fontsize=20)
        plt.xlabel('{0}'.format(param), fontsize=20)
        fig.savefig(savefolder + '{0} - Control Index.png'.format(param), bbox_inches='tight')
        plt.close()

    # we are done, no more processing needed
    pool.close()


def _get_max_trimmed_ay(ay_yaw_list, max_ay):
    max_trimmed_ay = 0.0
    interpolated = interpolate.interp1d([A_y for (A_y, yaw) in ay_yaw_list],
                                        [yaw for (A_y, yaw) in ay_yaw_list],
                                        kind='linear')

    def f(x):
        x = ay_yaw_list[0][0] if x < ay_yaw_list[0][0] else x
        x = ay_yaw_list[-1][0] if x > ay_yaw_list[-1][0] else x
        return interpolated(x)

    guess = max_ay
    delta = 0.001
    tolerance = 0.001
    while guess > max_trimmed_ay:
        if abs(f(guess)) < tolerance:
            max_trimmed_ay = guess
        guess -= delta
    return max_trimmed_ay
