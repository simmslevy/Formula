from B14.Car import B14
from CnAy.Plot import make_plot
from CnAy.SteeringFunctions import BasicSteeringFunction, AntiAckermanB14, AntiAckermanB14RearWheelSteering
from TireModel import tire_func
import numpy as np

def tire_func_b(x, y):
    return tire_func(x, y)

default_params = {'a_x': 0.0, # g's
                  'toe_in_front': 0.0, # degrees
                  'toe_in_rear': 0.0, # degrees
                  'wheelbase': B14.wheels.wheel_base_m, # meters
                  'track_front': B14.wheels.track_width_f_m, # meters
                  'track_rear': B14.wheels.track_width_r_m, # meters'
                  'cg_height': B14.cg_z_m, # meters
                  'car_lbs': B14.weight_lb, # lbs
                  'driver_lbs': 150, # lbs
                  'percent_rear_weight': 0.53,
                  'v_nom': 25.0, # m / s
                  'lltd': 0.5,
                  'steer_func': AntiAckermanB14(),
                  'tire_func': tire_func}

# for testing new features
make_plot(default_params, percent_rear_weight=np.linspace(0.5, 1.0, endpoint=True, num=11))

# huge batch job, takes at least an hour
#make_plot(default_params,
#          LLTD=np.linspace(0.00, 1.00, endpoint=True, num=101),
#          percent_rear_weight=np.linspace(0.01, 0.99, endpoint=True, num=99),
#          car_lbs=np.linspace(260, 400, endpoint=True, num=40),
#          toe_in_front=np.linspace(-2, 2, endpoint=True, num=41),
#          toe_in_rear=np.linspace(-2, 2, endpoint=True, num=41),
#          track_front=np.linspace(0.1, 2.0, endpoint=True, num=39),
#          track_rear=np.linspace(0.1, 2.0, endpoint=True, num=39),
#          wheelbase=np.linspace(0.1, 2.3, endpoint=True, num=45),
#          )
#

