from scipy import interpolate
from TrigHelpers import sign


class SteeringFunction():
    def get_rl(self, steer_angle):
        """
        Return the rear left tire angle as a function of steering angle
        :param steer_angle: angle measured at the steering wheel in degrees
        :return: tire angle in degrees
        """
        raise NotImplementedError()

    def get_rr(self, steer_angle):
        """
        Return the rear right tire angle as a function of steering angle
        :param steer_angle: angle measured at the steering wheel in degrees
        :return: tire angle in degrees
        """
        raise NotImplementedError()

    def get_fl(self, steer_angle):
        """
        Return the front left tire angle as a function of steering angle
        :param steer_angle: angle measured at the steering wheel in degrees
        :return: tire angle in degrees
        """
        raise NotImplementedError()

    def get_fr(self, steer_angle):
        """
        Return the front right tire angle as a function of steering angle
        :param steer_angle: angle measured at the steering wheel in degrees
        :return: tire angle in degrees
        """
        raise NotImplementedError()


class BasicSteeringFunction(SteeringFunction):
    def get_fl(self, steer_angle):
        return steer_angle

    def get_fr(self, steer_angle):
        return steer_angle

    def get_rl(self, steer_angle):
        return 0.0

    def get_rr(self, steer_angle):
        return 0.0


class AntiAckermanB14(SteeringFunction):

    # this is here and not in __init__ because we need to be able to pickle AntiAckermanB14Interpolated
    steer_angles = []
    tire_angles = []
    with open('anti ackerman raw steer data b14.csv') as f:
        for line in f.read().split('\n')[1:]:
            steer_angles.append(float(line.split(',')[1]))
            tire_angles.append(float(line.split(',')[2]))

    AntiAckermanB14Interpolated = interpolate.interp1d(steer_angles, tire_angles, kind='linear')

    def get_fl(self, steer_angle):
        return -self.get_fr(-steer_angle)

    def get_fr(self, steer_angle):
        return self.__class__.AntiAckermanB14Interpolated(steer_angle)

    def get_rl(self, steer_angle):
        return 0.0

    def get_rr(self, steer_angle):
        return 0.0


class AntiAckermanB14RearWheelSteering(AntiAckermanB14):
    def __init__(self, max_rear_angle=3.0):
        self.max_rear_angle = max_rear_angle

    def get_rl(self, steer_angle):
        angle = self.get_fr(steer_angle)
        return -sign(angle) * min(abs(angle), self.max_rear_angle)

    def get_rr(self, steer_angle):
        angle = self.get_fr(steer_angle)
        return -sign(angle) * min(abs(angle), self.max_rear_angle)
