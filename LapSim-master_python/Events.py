from utils import memoize
from math import pi
import Constants
import matplotlib.pyplot as plt
import numpy as np


class Feature():
    def __init__(self):
        self.length = None

    def __hash__(self):
        return 17 * 31 + hash(self.length)

    def time(self, car, start_velocity, next_feature, dt=0.001):
        raise NotImplementedError("Time method is not implemended")


class Corner(Feature):
    def __init__(self, radius, length):
        self.radius = radius
        self.length = length

    def __hash__(self):
        result = 17
        result = result * 31 + hash(self.length)
        result = result * 31 + hash(self.radius)
        return int(result)

    def time(self, car, start_velocity, next_feature, dt=0.001):
        v_corner = car.corner_velocity(self.radius)
        if start_velocity < v_corner:
            v_corner = (start_velocity + v_corner) / 2.0
        corner_time, yaws, lat_gs = car.corner_time(self.radius, self.length, v_corner)

        corner_rpm = car.engine.current_rpm(v_corner)[0]
        # TODO fuel
        fuel = 0
        brake_time = 0
        nshifts = 0
        return (corner_time, nshifts, v_corner, fuel, brake_time,
                [v_corner for _ in range(len(lat_gs))], [corner_rpm for _ in range(len(lat_gs))], lat_gs, yaws)


class Straight(Feature):
    def __init__(self, length):
        """
        :param length: length of the straight in meters
        :return: an instance of the Straight object
        """
        self.length = length

    def time(self, car, start_velocity, next_feature, dt=0.001):
        """
        :param car: the car that is driving this straight
        :param start_velocity: the velocity that the car starts at
        :param next_feature: the track feature that happens after this straight
        :param dt: timestep for calculations
        :return: time need to drive the straight, number of gear shifts that occur, velocity at the end of the straight,
        fuel used during the straight, time spent braking at the end of the straight, a list of all velocities from
        the straight, a list of all rpms from the straight, a list of all lateral accelerations from the straight, a
        list of all yaw accelerations from the straight.
        """
        if next_feature == EndFeature:
            v_end_max = car.top_speed / Constants.MPHPerms
        else:
            v_end_max = car.corner_velocity(next_feature.radius)

        if v_end_max > car.top_speed * Constants.MS_PER_MPH:
            raise ValueError("v_end_max ({0}) is more than the car's top speed ({1})".format(v_end_max,
                                                                                             car.top_speed *
                                                                                             Constants.MS_PER_MPH))

        if start_velocity > car.top_speed * Constants.MS_PER_MPH:
            raise ValueError("start_velocity ({0}) is more than the car's top speed ({1})".format(start_velocity,
                                                                                                  car.top_speed *
                                                                                                  Constants.MS_PER_MPH))
        t = 0.0
        v = start_velocity
        nshift = 0.0
        tshift = 0.2
        fuel = 0.0
        length = self.length

        velocities = []
        rpms = []

        # TODO(low): There should be a smarter way of doing this loop
        brake_accel = Constants.g * car.braking_g
        brake_time = (v - v_end_max) / brake_accel
        brake_dist = v * brake_time - brake_accel * (brake_time ** 2.0) / 2.0

        rpm, gear = car.engine.current_rpm(v)
        while brake_dist < length:
            gear_old = gear
            rpm, gear = car.engine.current_rpm(v)
            velocities.append(v)
            rpms.append(rpm)

            if rpm > car.engine.redline:
                rpm = car.engine.redline
                v = (car.wheels.tyre_radius_m * car.engine.redline * Constants.RPMToRad /
                     (car.engine.final_drive * car.engine.primary_gear * gear))

            # see if we switched gears
            if gear != gear_old:

                # we dont shift if we will reach our corner after switching and wont have time to brake
                if (brake_dist > 0 and v * tshift * 2.5 >= (length - brake_dist)) \
                        or (brake_dist <= 0 and v * tshift * 2.5 >= lrem):
                    gear = gear_old
                    rpm = car.engine.redline
                    v = (car.wheels.tyre_radius_m * car.engine.redline * Constants.RPMToRad /
                         (car.engine.final_drive * car.engine.primary_gear * gear))

                # if we do shift
                else:
                    nshift += 1.0
                    t += tshift
                    length -= v * tshift

                    #if clutch == False and rpm < car.engine.clutch_engage_rpm:
                    #    F_accel = (car.engine.torque(car.engine.clutch_engage_rpm) * Constants.NM_PER_LB_FT *
                    #               car.engine.final_drive * car.engine.primary_gear * car.engine.gears[gear] *
                    #               car.engine.drivetrain_efficiency / car.wheels.tyre_radius_m)
                    #if clutch == True and rpm < car.engine.max_torque_rpm:
                    #    F_accel = (max_torque * car.engine.final_drive * car.engine.primary_gear *
                    #               car.engine.gears[gear] * car.engine.drivetrain_efficiency /
                    #               car.wheels.tyre_radius_m)
                    #if (clutch == True and rpm >= car.engine.max_torque_rpm) or
                    #   (clutch == False and rpm > car.engine.clutch_engage_rpm):
                    #    F_accel = (car.engine.torque(rpm) * Constants.NM_PER_LB_FT * car.engine.final_drive *
                    #               car.engine.primary_gear * car.engine.gears[gear] *
                    #               car.engine.drivetrain_efficiency() / car.wheels.tyre_radius_m)

            accel_begin = 1.0 / car.effective_mass * (car.engine.torque_nm(rpm) * car.engine.drivetrain_efficiency
                                                      * rpm * Constants.RPMToRad / v - car.drag(v) -
                                                      car.rolling_resistance(v))
            v_mid_dt = v + accel_begin * dt / 2.0
            rpm_mid_dt, ignore_the_gear = car.engine.current_rpm(v_mid_dt)
            accel_mid_dt = 1.0 / car.effective_mass * (car.engine.torque_nm(rpm_mid_dt) *
                                                       car.engine.drivetrain_efficiency * rpm_mid_dt *
                                                       Constants.RPMToRad / v_mid_dt - car.drag(v_mid_dt) -
                                                       car.rolling_resistance(v_mid_dt))
            v += accel_mid_dt * dt
            length -= v_mid_dt * dt
            t += dt
            fuel += (car.engine.bsfc * dt * car.engine.torque(rpm_mid_dt) * car.engine.drivetrain_efficiency
                     * rpm_mid_dt / 5252.0)

            brake_time = (v - v_end_max) / brake_accel
            brake_dist = v * brake_time - brake_accel * (brake_time ** 2.0) / 2.0

            # TODO(low) do we need this?
            if length <= 0.1:
                brake_time = 0.0
                v_end_max = v
                t += length / v
                length = 0.0

        t += brake_time
        # TODO make graphing optional
        for _ in range(int(brake_time / dt)):
            v = v - brake_accel * dt
            velocities.append(v)
            rpms.append(car.engine.current_rpm(v)[0])

        return (t, nshift, v_end_max, fuel, brake_time, velocities, rpms,
                [0 for _ in range(len(velocities))], [0 for _ in range(len(velocities))])


class EndFeature(Feature):
    pass

EndFeature = EndFeature()


class Event():
    class ConstructionError(Exception):
        pass

    def __init__(self, winning_time, num_laps):
        self._num_laps = num_laps
        self._features = []
        self.winning_time = winning_time

        self._laptime = 0.0
        self._tcorners = None
        self._tstraights = None
        self._fuel_used = None
        self._tbraking = None

        # for plotting
        self.velocities = []
        self.rpms = []
        self.yaws = []
        self.lat_gs = []

    def __hash__(self):
        result = 17.0
        result = result * 31 + hash(self._num_laps)
        result = result * 31 + hash(self.winning_time)
        for feature in self._features:
            result = result * 31 + hash(feature)
        return int(result)

    def __eq__(self, other):
        return (other is not None and
                isinstance(other, Event) and
                other._num_laps == self._num_laps and
                other._featuers == self._features and
                other.winning_time == self.winning_time
                )

    def __ne__(self, other):
        return not self == other

    def add_feature(self, feature):
        # we cannot have two straight in a row
        if len(self._features) > 0 and isinstance(feature, Straight) and isinstance(self._features[-2], Straight):
            raise Event.ConstructionError("Cannot have two straights in a row.  Just make one longer straight.")
        self._features = self._features[:-1] + [feature, EndFeature]

    @property
    def _num_features(self):
        return len(self._features) - 1

    def _compute_event(self, car):
        raise NotImplementedError("Please implement this method")

    def get_points(self, car):
        raise NotImplementedError("Please implement this method")

    def time_straights(self, car):
        return self._compute_event(car)["time_straights"]

    def time_corners(self, car):
        return self._compute_event(car)["time_corners"]

    def time_braking(self, car):
        return self._compute_event(car)["time_braking"]

    def fuel_used(self, car):
        return self._compute_event(car)["fuel_used"]

    def event_time(self, car):
        return self._compute_event(car)["event_time"]


class Endurance(Event):
    def fuel_score(self, car):
        t_your = self.event_time(car)
        t_min = min(self.winning_time, t_your)
        fuel_factor = (100.0 * (t_min / t_your) * (min(4.849, self.fuel_used(car) * 2.31 * 3.78541) /
                                                   (self.fuel_used(car) * 2.31 * 3.78541)))
        fuel_factor_min = 100.0 * (1.0 / 1.45) * (min(4.849, self.fuel_used(car) * 2.31 * 3.78541) / 13.2132)

        print(100.0 * (fuel_factor_min / fuel_factor - 1.0) / (fuel_factor_min / 100.0 - 1.0))
        return 100.0 * (fuel_factor_min / fuel_factor - 1.0) / (fuel_factor_min / 100.0 - 1.0)

    def get_points(self, car):
        """
        Return the number of points that the car will get in this event given a fastest for the event.
        :param car: We use this car to get a time for this event and then compute the number of points scored.
        :return: The number of points scored in this event

        From the 2014 FSAE Rules - Section D8.20.2 (Page 154)
        """
        t_min = min(self.winning_time, self.event_time(car))
        t_max = 1.45 * t_min
        t_your = self.event_time(car)
        if t_your > t_max:
            return 0.0
        return 250.0 * ((t_max / t_your) - 1.0) / ((t_max / t_min) - 1.0) + 50.0

    @memoize
    def _compute_event(self, car):
        """

        :param car: the car that we want to run this event
        """
        self._laptime = 0.0
        v_last_feature = car.corner_velocity(self._features[self._num_features - 1].radius)
        self._tstraights, self._tcorners, self._fuel_used, self._tbraking = 0.0, 0.0, 0.0, 0.0
        dista = 0.0
        velocities, rpms, yaws, lat_gs = [], [], [], []
        for i in range(self._num_features):
            feature = self._features[i]
            next_feature = self._features[i+1]

            if isinstance(feature, Straight):
                # the next feature is a corner because two straights in a row is just a longer straight
                # this is enforced during event construction
                v_straight_end_max = car.corner_velocity(next_feature.radius)
                t, nshift, v_last_feature, fuel, brake_time, velocities_, rpms_ = car.straight_time(feature.length,
                                                                                                    v_last_feature,
                                                                                                    v_straight_end_max)
                self._laptime += t
                self._tstraights += t
                self._tbraking += brake_time
                self._fuel_used += fuel
                velocities += velocities_
                rpms += rpms_
                lat_gs += [0 for _ in range(len(velocities_))]
                yaws += [0 for _ in range(len(velocities_))]

            elif isinstance(feature, Corner):
                dista += feature.length
                v_corner = car.corner_velocity(feature.radius)
                if v_last_feature < v_corner:
                    v_last_feature = (v_last_feature + v_corner) / 2.0
                else:
                    v_last_feature = v_corner
                corner_time = car.corner_time(feature.radius, feature.length, v_last_feature)
                self._laptime += corner_time
                self._tcorners += corner_time

                corner_rpm = car.engine.current_rpm(v_corner)[0]
                for _ in range(int(corner_time / 0.001)):
                    velocities.append(v_corner)
                    rpms.append(corner_rpm)
                    yaws.append(0.0)
                    lat_gs.append(v_corner ** 2.0 / feature.radius / Constants.g)

        results = {"event_time": self._laptime * self._num_laps,
                   "time_corners": self._tcorners * self._num_laps,
                   "time_straights": self._tstraights * self._num_laps,
                   "fuel_used": self._fuel_used * self._num_laps * (1.0 + self._tcorners / self._tstraights / 2.0)}
        print(results)

        plot_traces(rpms, velocities, yaws, lat_gs, title='Endurance')
        return results


class Autocross(Event):
    
    def __init__(self, winning_time):
        # an autocross is an event with 1 lap
        super().__init__(winning_time=winning_time, num_laps=1)

    def get_points(self, car):
        """
        Return the number of points that the car will get in this event given a fastest time for the event.
        :param car: We use this car to get a time for this event and then compute the number of points scored.
        :return: The number of points scored in this event

        From the 2014 FSAE Rules - Section D7.8.1 (Page 148)
        """
        t_your = self.event_time(car)
        t_min = min(self.winning_time, t_your)
        t_max = 1.45 * t_min
        if t_your > t_max:
            return 7.5
        return 142.5 * ((t_max / t_your) - 1.0) / ((t_max / t_min) - 1.0) + 7.5

    @memoize
    def _compute_event(self, car):
        """

        :param car: the car that we want to run this event
        """
        self._laptime = 0.0
        v_last_feature = car.launch_velocity_and_time(accel_dist=6.0)[0]
        self._tstraights, self._tcorners, self._fuel_used, self._tbraking = 0.0, 0.0, 0.0, 0.0

        for i in range(self._num_features):
            feature = self._features[i]
            next_feature = self._features[i+1]

            # TODO nshifts seems not implemented
            t, nshift, v_last_feature, fuel, brake_time, velocities, rpms, lat_gs, yaws = feature.time(car, v_last_feature, next_feature, dt=0.001)
            self._laptime += t
            self._tbraking += brake_time
            self._fuel_used += fuel
            self.velocities += velocities
            self.rpms += rpms
            self.lat_gs += lat_gs
            self.yaws += yaws

        results = {"event_time": self._laptime * self._num_laps,
                   "time_corners": self._tcorners * self._num_laps,
                   "time_straights": self._tstraights * self._num_laps}
                   #"fuel_used": self._fuel_used * self._num_laps * (1.0 + self._tcorners / self._tstraights / 2.0)}

        plot_traces(self.rpms, self.velocities, self.yaws, self.lat_gs, title='Autocross')
        plt.hist(self.lat_gs, bins=400)
        plt.show()
        return results


class Skidpad(Event):
    def __init__(self, winning_time):
        super().__init__(winning_time=winning_time, num_laps=1)
        self.add_feature(Corner(radius=17.1 / 2.0, length=17.1 * pi))

    def get_points(self, car):
        """
        Return the number of points that the car will get in skidpad given a fastest time for the event.
        :param car: We use this car to get a time for this event and then compute the number of points scored.
        :return: The number of points scored in this event

        From the 2014 FSAE Rules - Section D6.8.3 (Page 146)
        """
        t_your = self.event_time(car)
        t_min = min(self.winning_time, t_your)
        t_max = 1.25 * t_min
        if t_your > t_max:
            return 2.5
        return 47.5 * ((t_max / t_your) ** 2.0 - 1.0) / ((t_max / t_min) ** 2.0 - 1.0) + 2.5

    @memoize
    def _compute_event(self, car):
        feature = self._features[0]
        v_corner = car.corner_velocity(feature.radius)
        self._laptime = feature.length / v_corner

        results = {"event_time": self._laptime * self._num_laps,
                   "time_corners": self._laptime * self._num_laps}
        return results


class Acceleration(Autocross):
    def __init__(self, winning_time):
        super().__init__(winning_time=winning_time)

    @memoize
    def _compute_event(self, car, dt=0.001):
        results = {"event_time": car.launch_velocity_and_time(dt=dt, accel_dist=75.0)[1]}
        return results

    def get_points(self, car):
        """
        Return the number of points that the car will get in acceleration given a fastest time for the event.
        :param car: We use this car to get a time for this event and then compute the number of points scored.
        :return: The number of points scored in this event

        From the 2014 FSAE Rules - Section D5.8.2 (Page 144)
        """
        t_your = self.event_time(car)
        t_min = min(self.winning_time, t_your)
        t_max = t_min * 1.5
        if t_your > t_max:
            return 3.5
        return 71.5 * ((t_max / t_your) - 1.0) / ((t_max / t_min) - 1.0) + 3.5


# TODO move this
def plot_traces(rpms, velocities, yaws, lat_gs, title='', dt=0.001):
    # timestamps
    timestamps = np.arange(0, len(rpms) * dt, step=dt)

    # plot
    f, (ax_rpm, ax_v, ax_yaw, ax_lat_g) = plt.subplots(4, 1, sharex=True)

    ax_rpm.set_title(title)
    ax_rpm.plot(timestamps, rpms, 'b')
    ax_rpm.set_ylabel('RPM [rpm]')
    ax_rpm.grid(axis='x')

    ax_v.plot(timestamps, velocities, 'b')
    ax_v.set_ylabel('Velocity [m/s]')
    ax_v.grid(axis='x')

    ax_yaw.plot(timestamps, yaws, 'b')
    ax_yaw.set_ylabel('Angular Accel []')
    ax_yaw.grid(axis='x')

    ax_lat_g.plot(timestamps, lat_gs, 'b')
    ax_lat_g.set_ylabel('Lat Accel [g]')
    ax_lat_g.set_xlabel('Time [s]')
    ax_lat_g.grid(axis='x')

    plt.show()