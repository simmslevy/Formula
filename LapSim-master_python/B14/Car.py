from Car import Car
from Engine import Engine
from Wheel import Wheel
from Aero import no_aero
import Constants

wheels = Wheel(diameter_in=10.0,
               wheel_base_in=60.0,
               track_width_f=45.0,
               track_width_r=45.0,
               tyre_data=None)

gears = [1.0, 1.0]
final_drive = wheels.tyre_radius_m * 12500.0 * Constants.RPMToRad / 51.0 / Constants.MS_PER_MPH
engine = Engine(redline=12500,
                gears=gears,
                final_drive=final_drive,
                drivetrain_efficiency=0.8,
                clutch_engage_rpm=5500)

engine.add_torque_curve_point(0, 7.375621)
engine.add_torque_curve_point(6011.75, 15.72829051)
engine.add_torque_curve_point(6506.38, 17.65790048)
engine.add_torque_curve_point(7014.79, 19.4747372)
engine.add_torque_curve_point(7509.66, 20.38702776)
engine.add_torque_curve_point(8004.53, 21.29931832)
engine.add_torque_curve_point(8513.47, 20.8553797)
engine.add_torque_curve_point(8981.11, 20.63684005)
engine.add_torque_curve_point(9503.97, 19.51493434)
engine.add_torque_curve_point(9985.52,  18.6184276)
engine.add_torque_curve_point(10494.7, 17.38323235)
engine.add_torque_curve_point(10990.1, 16.03474757)
engine.add_torque_curve_point(11485.5, 14.79940481)
engine.add_torque_curve_point(11980.8, 13.79005107)
engine.add_torque_curve_point(12489.9, 12.55485582)
engine.add_torque_curve_point(12999.1, 10.98060328)

B14 = Car(weight_lb=280.0, weight_dist=0.47, cg_z_in=11.7, wheels=wheels, engine=engine, aero=no_aero, braking_g=1.36,
          yaw_accel=10.0, cla=0.0, cda=0.0, lat_g=1.36)

def B14_with_driver(driver_weight):
    return Car(weight_lb=280.0 + driver_weight, weight_dist=0.47, cg_z_in=11.7, wheels=wheels, engine=engine,
               aero=no_aero, braking_g=1.36, yaw_accel=10.0, cla=2.0, cda=2.0, lat_g=1.36)
