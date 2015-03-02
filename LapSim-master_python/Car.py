import scipy.optimize
import Constants
import math
from Engine import Engine
from Aero import Aero
from Wheel import Wheel
from utils import memoize


class Car():
    def __init__(self, weight_lb, weight_dist, cg_z_in, wheels, engine, aero, braking_g, yaw_accel, cla, cda, lat_g):
        """
        :param weight_lb: weight of the self and driver (lbs)
        :param weight_dist: rearware from front axle (0 < weight_dist < 1)
        :param cg_z_in: cg height (in)
        :param wheels: an instance of the Wheel class
        :param engine: an instance of the Engine class
        :param aero: an instance of the Aero class
        :param braking_g: max braking acceleration (g)
        :param yaw_accel: angular yaw acceleration of the self (rad/s^2)
        :return: an instance of the Car class
        """
        if braking_g <= 0:
            raise ValueError("braking_g ({0}) cannot be negative or zero".format(braking_g))
        if lat_g <= 0:
            raise ValueError("latG ({0}) cannot be negative or zero".format(lat_g))
        if weight_lb <= 0:
            raise ValueError("weight_lb ({0}) cannot be negative or zero".format(weight_lb))
        if cg_z_in <= 0:
            raise ValueError("cg_z_in ({0}) cannot be negative or zero".format(cg_z_in))
        if yaw_accel <= 0:
            raise ValueError("yaw_accel ({0}) cannot be negative or zero".format(yaw_accel))
        if not isinstance(engine, Engine):
            raise TypeError("engine ({0}) must be an instance of Engine".format(type(engine)))

        try:
            engine.torque(1.0)
        except ValueError:
            raise ValueError("engine doesn't have a torque curve!")

        if not isinstance(wheels, Wheel):
            raise TypeError("wheels ({0}) must be an instance of Wheel".format(type(wheels)))
        if not isinstance(aero, Aero):
            raise TypeError("aero ({0}) must be an instance of Aero".format(type(aero)))

        self._engine = engine
        self._engine._car = self
        self._aero = aero
        self._wheels = wheels
        self._weight_lb = weight_lb
        self._weight_dist = weight_dist
        self._cg_z_in = cg_z_in
        self._braking_g = braking_g
        self._yaw_accel = yaw_accel
        self._cDA = cda
        self._cLA = cla
        self._latG = lat_g

    def __hash__(self):
        result = 17.0
        result = result * 31 + hash(self._engine)
        result = result * 31 + hash(self._aero)
        result = result * 31 + hash(self._wheels)
        result = result * 31 + hash(self._weight_lb)
        result = result * 31 + hash(self._weight_dist)
        result = result * 31 + hash(self._cg_z_in)
        result = result * 31 + hash(self._braking_g)
        result = result * 31 + hash(self._yaw_accel)
        result = result * 31 + hash(self._cDA)
        result = result * 31 + hash(self._cLA)
        result = result * 31 + hash(self._latG)
        return int(result)

    def __eq__(self, other):
        # TOOD fix this
        return (other is not None and
                isinstance(other, Car) and
                other.engine == self.engine and
                other.aero == self.aero and
                other.wheels == self.wheels and
                other.weight_lb == self.weight_lb and
                other.weight_dist == self.weight_dist and
                other.cg_z_in == self.cg_z_in and
                other.braking_g == self.braking_g and
                other.yaw_accel == self.yaw_accel and
                other.cDA == self.cDA and
                other.cLA == self.cLA and
                other.latG == self.lat_g)

    @property
    def top_speed(self):
        """
        Use the engine redline and highest gear to calculate this self's top speed.
        :return: this self's top speed (MPH)
        """
        # TODO check this
        return (self.wheels.tyre_radius_m * self.engine.redline * Constants.RPMToRad / (self.engine.primary_gear * self.engine.gears[-2] * self.engine.final_drive * Constants.MS_PER_MPH))

    @property
    def braking_g(self):
        return self._braking_g

    @property
    def yaw_accel(self):
        return self._yaw_accel

    @property
    def cg_z_in(self):
        return self._cg_z_in

    @property
    def cg_z_m(self):
        return self.cg_z_in * Constants.M_PER_INCH

    @property
    def aero(self):
        return self._aero

    @property
    def engine(self):
        return self._engine

    @property
    def wheels(self):
        return self._wheels

    @property
    def weight_lb(self):
        return self._weight_lb + self.aero.weight_lb

    @property
    def mass_kg(self):
        return self.weight_lb * Constants.KG_PER_LB

    @property
    def weight_n(self):
        return self.mass_kg * Constants.g

    @property
    def weight_dist(self):
        return self._weight_dist

    @property
    def c_length(self):
        return self.wheels.wheel_base_m() * self.weight_dist

    @property
    def b_length(self):
        return self.wheels.wheel_base_m() * (1 - self.weight_dist())

    @property
    def effective_mass(self):
        return self.mass_kg + (self.wheels.rotational_inertia / (self.wheels.tyre_radius_m ** 2.0))

    # TODO redundant code, see Aero.py
    def drag(self, velocity):
        return (Constants.RHOAIR / 2.0) * (velocity ** 2.0) * self.c_da

    # TODO I want to use Aero.py for this
    @property
    def c_da(self):
        return self._cDA

    def lift(self, velocity):
        """

        :param velocity: m/s
        :return: downforce in N
        """
        return Constants.RHOAIR / 2.0 * (velocity ** 2.0) * self.c_la

    @property
    def c_la(self):
        return self._cLA

    def rolling_resistance(self, velocity):
        """Equation from from Gillespie p 117"""
        if velocity < 0.0:
            raise ValueError("Velocity ({0}) cannot be negative".format(velocity))
        result = self.weight_n * (0.018 + 3.24 * 0.013 * ((velocity * Constants.MPHPerms / 100.0) ** 2.5))
        if result <= 0.0:
            raise RuntimeWarning("rolling_resistance ({0}) should not be negative or zero".format(result))
        return result

    @property
    @memoize
    def mu_b(self):
        def f(mu):
            dl = self._delta_l
            wd = self.weight_dist
            w = self.weight_lb
            return (mu * ((wd + dl) * (1.0 - 0.0009 * (wd + dl) / 2.0 * w) +
                          (1.0 - wd - dl) * (1.0 - 0.0009 * (1.0 - wd - dl) / 2.0 * w))
                    - self.braking_g)
        # TODO this is different than daves
        return 1.54223
        return scipy.optimize.broyden1(f, [0, 0])[1]

    @property
    @memoize
    def mu_c(self):
        def f(mu):
            dc = self._delta_c
            wd = self.weight_dist
            w = self.weight_lb
            return (mu * ((wd + dc) / 2.0 * (1 - 0.0009 * (wd + dc) / 2.0 * w) +
                          (wd - dc) / 2.0 * (1 - 0.0009 * (wd - dc) / 2.0 * w) +
                          (1 - wd + dc) / 2.0 * (1 - 0.0009 * (1.0 - wd + dc) / 2.0 * w) +
                          (1 - wd - dc) / 2.0 * (1 - 0.0009 * (1.0 - wd - dc) / 2.0 * w))
                    - self._latG)

        return 1.59155
        return scipy.optimize.broyden1(f, [0])[0]

    def launch_velocity_and_time(self, accel_dist=6.0, dt=0.001):
        clutch = False  # is there a clutch?
        d, t = 0.0, 0.0
        nshifts = 0.0
        tshift = self.engine.shift_time
        trac_limited = True
        v = 0.0
        gear = 0

        wd = self.weight_dist
        h_cg = self.cg_z_m
        wheelbase = self.wheels.wheel_base_m

        f_accel = self.mu_b * (1.0 - wd) * self.weight_n * (1.0 - 0.0009 * (1.0 - wd) / 2.0 * self.weight_lb)

        if not f_accel > 0:
            raise RuntimeWarning("f_accel ({0}) should not be positive".format(f_accel))

        def f(force):
            return (force * Constants.nPerPound - self.mu_b * (1.0 - wd + h_cg / wheelbase * force / self.weight_lb) *
                    self.weight_n * (1.0 - 0.0009 * (1.0 - wd + h_cg / wheelbase * force / self.weight_lb) / 2.0
                                     * self.weight_lb))

        # same as daves
        f_accel_trac_limited = scipy.optimize.broyden1(f, [0], f_tol=0.000000000001)[0] * Constants.nPerPound

        if not f_accel > 0.0:
            raise RuntimeWarning("f_accel_trac_limited ({0}) should be positive".format(f_accel_trac_limited))

        max_torque = self.engine.max_torque_nm

        while trac_limited and d < accel_dist:
            v_prev = v
            # TODO check this is in m/s, it should be
            v += dt * (f_accel - self.drag(v_prev) - self.rolling_resistance(v_prev)) / self.effective_mass
            d += (v + v_prev) / 2.0 * dt
            t += dt
            f_accel = f_accel_trac_limited

            # correct
            rpm = self.engine.drivetrain_reduction(gear) * v / self.wheels.tyre_radius_m / Constants.RPMToRad

            # TODO(low): I do not like this len(self.engine.gears) nonsense
            # TODO RPMRAD check
            # do we need to shift?
            #if rpm >= self.engine.redline and gear != len(self.engine.gears) - 1:
            #    print("We shouldnt be shifting if we have a swissauto")
            #    gear += 1
            #    nshifts += 1
            #    t += tshift
            #    i = 0
            #    while i <= tshift and d <= accel_dist:
            #        v_prev = v
            #        v -= dt * (self.drag(v) + self.rolling_resistance(v)) / self.effective_mass
            #        d += (v + v_prev) * dt / 2
            #        i += dt
                 # check this
            #    rpm = self.engine.final_drive * self.engine.primary_gear * self.engine.gears[gear] * v / \
            #                      (self.wheels.tyre_radius_m * Constants.RPMToRad)

            # TODO(low): I do not like this len(self.engine.gears) nonsense
            # are we at redline in the highest gear?
            if rpm >= self.engine.redline and gear == len(self.engine.gears) - 2:
                while d < accel_dist:
                    d += v * dt
                    t += dt
                pass

            if clutch and rpm <= self.engine.max_torque_rpm:
                print("SA shouldnt get here")
                f_try = (max_torque * self.engine.drivetrain_reduction(gear) * self.engine.driveline_efficiency /
                         self.wheels.tyre_radius_m)
            elif not clutch and rpm < self.engine.clutch_engage_rpm:
                f_try = (self.engine.torque_nm(self.engine.clutch_engage_rpm) * self.engine.drivetrain_reduction(gear) *
                         self.engine.drivetrain_efficiency / self.wheels.tyre_radius_m)
            elif (not clutch and rpm >= self.engine.clutch_engage_rpm) or (clutch and rpm > self.engine.max_torque_rpm):
                f_try = (self.engine.torque_nm(rpm) * self.engine.drivetrain_reduction(gear) *
                         self.engine.drivetrain_efficiency / self.wheels.tyre_radius_m)
            trac_limited = f_try > f_accel

        while d < accel_dist:
            # TODO(low) again with the len(gears) stuff
            if rpm >= self.engine.redline:
                if gear != len(self.engine.gears) - 2 and (accel_dist - d) / v >= tshift:  # can we shift?
                    gear += 1.0
                    nshifts += 1.0
                    t += tshift
                    j = 0.0
                    while j <= tshift and d <= accel_dist:
                        v_prev = v
                        v -= dt / self.effective_mass * (self.drag(v) + self.rolling_resistance(v))
                        d += (v + v_prev) * dt / 2
                        # TODO(low): len(gear) shinanigans
                else:  # we cant shift
                    while d < accel_dist:
                        d += v * dt
                        t += dt
                    pass

            v_prev = v
            rpm = self.engine.drivetrain_reduction(gear) * v / self.wheels.tyre_radius_m / Constants.RPMToRad
            if not clutch and rpm < self.engine.clutch_engage_rpm:
                f_accel = (self.engine.torque_nm(self.engine.clutch_engage_rpm) * self.engine.drivetrain_reduction(gear)
                           * self.engine.drivetrain_efficiency / self.wheels.tyre_radius_m)
            if clutch and rpm < self.engine.max_torque_rpm:
                f_accel = (max_torque * self.engine.drivetrain_reduction(gear) * self.engine.drivetrain_efficiency /
                           self.wheels.tyre_radius_m)
            if (clutch and rpm >= self.engine.max_torque_rpm) or (not clutch and rpm >= self.engine.clutch_engage_rpm):
                f_accel = (self.engine.torque_nm(rpm) * self.engine.drivetrain_reduction(gear) *
                           self.engine.drivetrain_efficiency / self.wheels.tyre_radius_m)
            v += dt / self.effective_mass * (f_accel - self.drag(v) - self.rolling_resistance(v))
            d += (v + v_prev) * dt / 2.0
            t += dt
        return v, t

    def corner_velocity(self, r):
        """
        Takes in the radius of the turn (R).  Returns the highest velocity that the self can go around the corner.
        """
        v_calculated = scipy.optimize.broyden1(lambda v: math.sqrt(self._ay(v) * Constants.g * r) - v,
                                               [math.sqrt(r * Constants.g * 1.4)])[0]

        if v_calculated > self.top_speed * Constants.MS_PER_MPH:
            return self.top_speed * Constants.MS_PER_MPH
        return v_calculated

    # TODO support CnAy diagram
    def corner_time(self, corner_radius, corner_distance, corner_velocity):
        """
        Takes in a corner radius, a corner distance, and the corner velocity.  Returns
        the number of seconds that it takes to complete the corner.  This works by determining the steady state yaw
        angular velocity based on the corner velocity and radius.  It then calculates the time spent in yaw
        accleration.  The corner time is the time spent in yaw acceleration plus the time spent in steady state.
        """
        if corner_velocity <= 0.0:
            raise ValueError("corner_velocity ({0}) cannot be 0 or negative".format(corner_velocity))

        if corner_radius <= 0.0:
            raise ValueError("corner_radius ({0}) cannot be 0 or negative".format(corner_radius))

        omega_steady_state = corner_velocity / corner_radius
        yaw_time = omega_steady_state / self.yaw_accel
        corner_angle = corner_distance / corner_radius
        yaw_angle = self.yaw_accel * (yaw_time ** 2.0) / 2.0

        dt = 0.001
        yaws, lat_gs = [], []
        # if transient throughout the corner
        if 2.0 * yaw_angle > corner_angle:
            time = 2.0 * math.sqrt(corner_angle / self.yaw_accel)

            while yaw_time > yaw_time / 2.0:
                yaws.append(self.yaw_accel)
                # TODO make cornering more accurate
                lat_gs.append(0.0)
                yaw_time -= dt
            while yaw_time > 0.0:
                yaws.append(-self.yaw_accel)
                lat_gs.append(0.0)
                yaw_time -= dt
        # if we're steady state during the corner
        else:
            time = 2.0 * yaw_time + corner_radius * (corner_angle - 2.0 * yaw_angle) / corner_velocity

            x = 0
            while x < yaw_time:
                yaws.append(self.yaw_accel)
                lat_gs.append(0.0)
                x += dt
            x = 0
            while x < time - 2.0 * yaw_time:
                x += dt
                yaws.append(0.0)
                lat_gs.append(corner_velocity ** 2.0 / corner_radius / 9.8)
            x = 0
            while x < yaw_time:
                yaws.append(-self.yaw_accel)
                lat_gs.append(0.0)
                x += dt

        return time, yaws, lat_gs

    def _ay(self, v):
        def f(ay):
            tr = (self.wheels.track_width_f_m + self.wheels.track_width_r_m) / 2.0
            wd = self.weight_dist
            h_cg = self.cg_z_m
            lift = self.lift(v)
            w = self.weight_lb
            mu = self.mu_c
            n_per_lb = Constants.nPerPound

            return (((wd / 2.0 + h_cg / tr * ay / 2.0 + 1.0 / 4.0 * lift / (w * n_per_lb)) *
                     (1.0 - 0.0009 * (wd / 2.0 * w + h_cg / tr * ay / 2.0 * w + 1.0 / 4.0 * lift / n_per_lb)) +
                     (wd / 2.0 - h_cg / tr * ay / 2.0 + 1.0 / 4.0 * lift / (w * n_per_lb)) *
                     (1.0 - 0.0009 * (wd / 2.0 * w - h_cg / tr * ay / 2.0 * w + 1.0 / 4.0 * lift / n_per_lb)) +
                     ((1.0 - wd) / 2.0 + h_cg / tr * ay / 2.0 + 1.0 / 4.0 * lift / (w * n_per_lb)) *
                     (1.0 - 0.0009 * ((1.0 - wd) / 2.0 * w + h_cg / tr * ay / 2.0 * w + 1.0 / 4.0 * lift / n_per_lb)) +
                     ((1.0 - wd) / 2.0 - h_cg / tr * ay / 2.0 + 1.0 / 4.0 * lift / (w * n_per_lb)) *
                     (1.0 - 0.0009 * ((1.0 - wd) / 2.0 * w - h_cg / tr * ay / 2.0 * w + 1.0 / 4.0 * lift / n_per_lb))
                     ) * mu - ay)

        ay = scipy.optimize.broyden1(f, [1], f_tol=1e-10)[0]
        if ay < 0:
            raise RuntimeWarning("ay is negative, ay = {ay}".format(ay=ay))
        return ay

    @property
    def _delta_c(self):
        return self.cg_z_m * 2 / (self.wheels.track_width_f_m + self.wheels.track_width_r_m) * self._latG

    @property
    def _delta_l(self):
        return self.cg_z_m / self.wheels.wheel_base_m * self.braking_g

    def __str__(self):
        # TODO fix this, change to **locals()
        return "Mass (kg): {0}\n\tMass (lb): {1}\n\tWeight (N): {2}\n\tFront\
                Weight Distribution (%): {3}\n\tCG Height (in): {4}\n\tBrake Force:\
                {5}\n\tEffective Mass (lb): {7}\n\n\
                {8}\n\n{9}\n\n{10}".format(
            self.mass_kg(),
            self.weight_lb(),
            self.weight_n(),
            self.weight_dist(),
            self.cg_z_in(),
            self.brake_force(),
            self.polar_moment(),
            round(self.effective_mass / KG_PER_LB, 2),
            self.wheels,
            self.engine,
            self.aero
        )