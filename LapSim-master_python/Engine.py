import Constants
import numpy
import pylab
from scipy import interpolate
from utils import RangeFloat, memoize


class Engine:

    def __init__(self,
                 redline,
                 gears,
                 clutch_engage_rpm=5000,
                 final_drive=10.8,
                 drivetrain_efficiency=1.0,
                 shift_time=0.2,
                 normalize_torque_area=False):
        self._redline = redline
        self._drivetrain_efficiency = drivetrain_efficiency
        self._torque_curve_rpm = []
        self._torque_curve_torque = []
        self._gears = gears
        self._final_drive = final_drive
        self._car = None
        self._max_torque = None
        self._max_torque_rpm = None
        self._torque_curve_interpolated = None
        self._clutch_engage_rpm = clutch_engage_rpm
        self._normalize_torque_area = normalize_torque_area
        self._shift_time = shift_time

    @property
    def redline(self):
        """
        :return: the engine's redline in rpm
        """
        return self._redline

    @property
    def car(self):
        if self._car is None:
            raise AttributeError("Engine is not attached to a car!")
        return self._car

    @property
    def shift_time(self):
        return self._shift_time

    @property
    def clutch_engage_rpm(self):
        return self._clutch_engage_rpm

    @property
    def drivetrain_efficiency(self):
        return self._drivetrain_efficiency

    def add_torque_curve_point(self, rpm, torque):
        """
        Add a point to the engine's torque curve.
        :param rpm: RPM at which to add the point
        :param torque: Torque at which to add the point in lb/ft
        :return: nothing
        """
        self._torque_curve_rpm.append(rpm)
        self._torque_curve_torque.append(torque)
        self._torque_curve_interpolated = None
        self._max_torque = None
        self._max_torque_rpm = None

    def _torque(self, rpm):
        """
        Return the torque output of the engine for the given rpm.
        :param rpm: get the engine torque at this rpm
        :return: torque output of the engine in lb/ft
        """
        if rpm < min(self._torque_curve_rpm) or rpm > max(self._torque_curve_rpm):
            raise ValueError("RPM ({rpm}) out of bounds ({min}-{max})".format(rpm=rpm,
                                                                              min=min(self._torque_curve_rpm),
                                                                              max=max(self._torque_curve_rpm)))
        if not self._torque_curve_interpolated:
            self._torque_curve_interpolated = interpolate.interp1d(self._torque_curve_rpm,
                                                                   self._torque_curve_torque,
                                                                   kind='linear')
        return self._torque_curve_interpolated(rpm)

    # TODO docstring
    def torque(self, rpm):
        if not self._normalize_torque_area:
            return self._torque(rpm)
        return self._torque(rpm) * self._normalize_torque_area / self.torque_curve_area

    # TODO docstring
    def torque_nm(self, rpm):
        return self.torque(rpm) * Constants.NM_PER_LB_FT

    def plot_torque_curve(self):
        """
        Plot this engine's torque curve points as well as the torque curve interpolation.
        :return: nothing
        """
        x_vals = numpy.linspace(min(self._torque_curve_rpm), max(self._torque_curve_rpm), 10000)
        pylab.plot(self._torque_curve_rpm, self._torque_curve_torque, 'o', x_vals, [self.torque(x) for x in x_vals])
        pylab.ylabel('torque ft/lbs', fontsize=20)
        pylab.xlabel('rpm', fontsize=20)
        pylab.show()

    @property
    @memoize
    def torque_curve_area(self):
        total = 0.0
        dx = 0.5
        for x in numpy.arange(min(self._torque_curve_rpm), max(self._torque_curve_rpm), step=dx):
            total += dx * self._torque(x)
        return total

    # TODO(low): BSFC should not be hardcoded.
    @property
    def bsfc(self):
        """
        Return the lbs of fuel per hp for this engine
        """
        return 0.41 / 3600.0

    @property
    def final_drive(self):
        return self._final_drive

    # TODO(med): I dont like the way gears are done currently
    @property
    def gears(self):
        """
        Return the gear array.
        """
        return self._gears

    @property
    def primary_gear(self):
        """
        Return the number of teeth on the primary gear of the engine.
        """
        return self._gears[-1]

    @property
    def max_torque(self):
        """
        :return: the maximum amount of torque (ft/lb) that this engine can output given an optimal RPM
        """
        if not self._max_torque:
            for rpm in RangeFloat(min(self._torque_curve_rpm), max(self._torque_curve_rpm)):
                if not self._max_torque or self.torque(rpm) > self._max_torque:
                    self._max_torque = self.torque(rpm)
                    self._max_torque_rpm = rpm
        return self._max_torque

    @property
    def max_torque_nm(self):
        return self.max_torque * Constants.NM_PER_LB_FT

    @property
    def max_torque_rpm(self):
        """
        Return the RPM at which this engine outputs the most torque.
        """
        if not self._max_torque_rpm:
            # we do all the calculations for self._max_torque_rpm in the self.max_torque function
            self.max_torque()
        return self._max_torque_rpm

    def current_rpm(self, velocity):
        """
        Takes in a velocity.  Returns the optimal gear that the car should be using and what RPM the car
        would be if using that optimal gear.  This function picks the optimal gear by picking the lowest gear such that
        the engine RPM is still below redline.
        :param velocity: the velocity of the car in m/s
        :return: rpm, current gear
        """
        omega_axle = velocity / self.car.wheels.tyre_radius_m
        redline_rad = self.redline * Constants.RPMToRad

        # cycle through gears finding the lowest such that RPM is below redline
        optimal_gear = self.gears[-2]
        for gear in reversed(self.gears[:-1]):
            crank_vec = omega_axle * self.final_drive * self.primary_gear * gear
            if crank_vec <= redline_rad:
                optimal_gear = gear

        crank = omega_axle * self.final_drive * self.primary_gear * optimal_gear
        rpm = crank / Constants.RPMToRad
        return rpm, optimal_gear

    def drivetrain_reduction(self, gear):
        return self.final_drive * self.primary_gear * self.gears[gear]

    def __str__(self):
        string = "Powertrain:"
        string += "\n\tRedline RPM: {self.redline}".format(**locals())
        string += "\n\tFinal Drive: {self.final_drive}".format(**locals())
        string += "\n\tDT Efficiency: {self.drivetrain_efficiency}".format(**locals())
        string += "\n\tBSFC: {self.bsfc}".format(**locals())
        return string
