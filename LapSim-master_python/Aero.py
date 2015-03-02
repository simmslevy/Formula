from Constants import RHOAIR


class Aero():
    # TODO this module is not really used
    def __init__(self, weight_lb, drag_coeff, front_area, down_force_40_mph=0):
        """self.downForceAt40MPH=100*Vehicle.nPerPound"""
        self._front_area = front_area
        self._down_force_40_mph = down_force_40_mph
        self._drag_coeff = drag_coeff
        self._weight_lb = weight_lb

    @property
    def down_force_40_mph(self):
        return self._down_force_40_mph

    @property
    def lift_const(self):
        """get rid of magic numbers"""
        return self.down_force_40_mph / (17.88**2)

    @property
    def front_area(self):
        return self._front_area

    @property
    def drag_coeff(self):
        return self._drag_coeff

    @property
    def drag_const(self):
        return RHOAIR / 2.0 * self.drag_coeff * self.front_area

    @property
    def weight_lb(self):
        return self._weight_lb

    def down_force(self, velocity):
        return self.lift_const * (velocity ** 2)

    def drag_force(self, velocity):
        return self.drag_const * (velocity ** 2)

    def __str__(self):
        return ("Aero:\n\tDrag Coeff: {0}\n\tDrag Constant: {1}\n\tFrontal Area: {2}\n"
                "\tDownforce at 40MPH: {3}\n\tLift Constant: {4}}").format(self.drag_coeff,
                                                                           self.drag_const,
                                                                           self.front_area,
                                                                           self.down_force_40_mph,
                                                                           self.lift_const)

no_aero = Aero(weight_lb=0, drag_coeff=0, front_area=0, down_force_40_mph=0)