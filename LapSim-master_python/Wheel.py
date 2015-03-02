import Constants


class Wheel():
    WHEEL_MASS = {
        13: 16.8 / 2.2,
        10: 11.1 / 2.2,
        8: 9 / 2.2,
    }

    TYRE_RADIUS = {
        13: 10.25 * Constants.M_PER_INCH,
        10: 9.0 * Constants.M_PER_INCH,
        8: 7.5 * Constants.M_PER_INCH,
    }

    ROTATIONAL_INERTIA = {
        13: 1.314,
        10: 0.618,
        8: 0.33,
    }

    def __init__(self, diameter_in, wheel_base_in, track_width_f, track_width_r, tyre_data):
        self._diameter_in = diameter_in
        self._wheel_base_in = wheel_base_in
        self._track_width_f = track_width_f
        self._track_width_r = track_width_r
        self._tyre_data = tyre_data

    @property
    def diameter_m(self):
        return self._diameter_in * Constants.M_PER_INCH

    @property
    def wheel_base_m(self):
        return self._wheel_base_in * Constants.M_PER_INCH

    @property
    def track_width_r_m(self):
        return self._track_width_r * Constants.M_PER_INCH

    @property
    def track_width_f_m(self):
        return self._track_width_f * Constants.M_PER_INCH

    @property
    def tyre_data(self):
        return self._tyre_data

    @property
    def mass_kg(self):
        return Wheel.WHEEL_MASS[self._diameter_in]

    @property
    def tyre_radius_m(self):
        return Wheel.TYRE_RADIUS[self._diameter_in]

    @property
    def rotational_inertia(self):
        return Wheel.ROTATIONAL_INERTIA[self._diameter_in]

    def __str__(self):
        string = "Wheel Diameter (in): {0}".format(self._diameter_in)
        string += "\n\tTyre Radius (in): {0}".format(self.tyre_radius_m / Constants.M_PER_INCH)
        string += "\n\tWheel Base (in): {0}".format(self._wheel_base_in)
        string += "\n\tTrack Front (in): {0}".format(self._track_width_f)
        string += "\n\tTrack Rear (in): {0}".format(self._track_width_r)
        string += "\n\tWheel Rotational Inertia (kg*m^2): {0}".format(self.rotational_inertia)
        return string