__author__ = 'gpearman'

from math import cos, sin, tan, acos, asin, atan, atan2, degrees, radians
import numpy as np


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle


def sign(x):
    if x >= 0:
        return 1
    return -1


def cosd(x):
    return cos(radians(x))


def sind(x):
    return sin(radians(x))


def tand(x):
    return tan(radians(x))


def acosd(x):
    return degrees(acos(x))


def asind(x):
    return degrees(asin(x))


def atand(x):
    return degrees(atan(x))


def atan2d(y, x):
    return degrees(atan2(y, x))