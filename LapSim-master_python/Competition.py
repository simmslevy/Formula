class Competition:
    def __init__(self, accel_event, skidpad_event, autocross_event, endurance_event, efficiency_points=95,
                 static_points=253):
        self.accel_event = accel_event
        self.skidpad_event = skidpad_event
        self.autocross_event = autocross_event
        self.endurance_event = endurance_event
        self.efficiency_points = efficiency_points
        self.static_points = static_points

    def __hash__(self):
        result = 17.0
        result = result * 31 + hash(self.accel_event)
        result = result * 31 + hash(self.skidpad_event)
        result = result * 31 + hash(self.autocross_event)
        result = result * 31 + hash(self.endurance_event)
        result = result * 31 + hash(self.efficiency_points)
        result = result * 31 + hash(self.static_points)
        return int(result)

    def __eq__(self, other):
        return (other is not None and
                isinstance(other, Competition) and
                other.accel_event == self.accel_event and
                other.skippad_event == self.skidpad_event and
                other.autocross_event == self.autocross_event and
                other.endurance_event == self.endurance_event and
                other.efficiency_points == self.efficiency_points and
                other.static_points == self.static_points)

    def __ne__(self, other):
        return not self == other

    def get_points(self, car, accel_car):
        """
        :param car: the car to use in the competition
        :return: the number of points the car scores at this competition
        """
        return (self.accel_event.get_points(accel_car) + self.skidpad_event.get_points(car) +
               self.autocross_event.get_points(car) + self.endurance_event.get_points(car) + self.efficiency_points +
               self.static_points)