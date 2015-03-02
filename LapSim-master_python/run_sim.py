__author__ = 'gpearman'
from B14.Events import autocross, endurance, skidpad, acceleration, comp
from B14.Car import B14, engine, wheels, B14_with_driver
import numpy
from Plotter import plot_colored_by_points, contour_plot, plot_many_y_funcs
from Car import Car
from Engine import Engine
from Aero import no_aero
import traceback
import Constants

#print(B14.launch_velocity())
#print(autocross.event_time(B14_with_driver(150.0)))
#print(B14_with_driver(150.0).corner_velocity(12.35))
#print(B14.straight_time(1000, 0.0, 22))
#print(endurance.fuel_used(B14))
#print(skidpad.event_time(B14_with_driver(150.0)))
#print(endurance.event_time(B14_with_driver(150.0)))
#print(B14_with_driver(150.0).straight_time(10.0, 10, 20))
#print(B14_with_driver(150.0).engine.current_rpm(10))

def F_cg(x):
    car = Car(weight_lb=300.0 + 150.0,
              weight_dist=x,
              cg_z_in=11.7,
              wheels=wheels,
              engine=engine,
              aero=no_aero,
              braking_g=1.36,
              yaw_accel=15,
              cda=2.0,
              cla=2.0,
              lat_g=1.36)
    accel_car = Car(weight_lb=300.0 + 110.0,
                    weight_dist=x,
                    cg_z_in=11.7,
                    wheels=wheels,
                    engine=engine,
                    aero=no_aero,
                    braking_g=1.36,
                    yaw_accel=15,
                    cda=2.0,
                    cla=2.0,
                    lat_g=1.36)
    try:
        return comp.get_points(car, accel_car)
    except: traceback.print_exc()

def F_yaw_latg(x, y):
    car = Car(weight_lb=300.0 + 150.0,
              weight_dist=0.47,
              cg_z_in=11.7,
              wheels=wheels,
              engine=engine,
              aero=no_aero,
              braking_g=1.36,
              yaw_accel=x,
              cda=2.0,
              cla=2.0,
              lat_g=y)
    accel_car = Car(weight_lb=300.0 + 110.0,
                    weight_dist=0.47,
                    cg_z_in=11.7,
                    wheels=wheels,
                    engine=engine,
                    aero=no_aero,
                    braking_g=1.36,
                    yaw_accel=x,
                    cda=2.0,
                    cla=2.0,
                    lat_g=y)
    try:
        return comp.get_points(car, accel_car)
    except: traceback.print_exc()
def F_cla_cda(y, x):
    car = Car(weight_lb=300.0 + 150.0,
              weight_dist=0.47,
              cg_z_in=11.7,
              wheels=wheels,
              engine=engine,
              aero=no_aero,
              braking_g=1.36,
              yaw_accel=30,
              cda=x,
              cla=y,
              lat_g=1.36)
    accel_car = Car(weight_lb=300.0 + 110.0,
                    weight_dist=0.47,
                    cg_z_in=11.7,
                    wheels=wheels,
                    engine=engine,
                    aero=no_aero,
                    braking_g=1.36,
                    yaw_accel=30,
                    cda=x,
                    cla=y,
                    lat_g=1.36)
    try:
        return comp.get_points(car, accel_car)
    except: traceback.print_exc()


def cg_aero(x):
    car = Car(weight_lb=300.0 + 150.0,
              weight_dist=0.47,
              cg_z_in=x,
              wheels=wheels,
              engine=engine,
              aero=no_aero,
              braking_g=1.36,
              yaw_accel=15,
              cda=2.0,
              cla=2.0,
              lat_g=1.36)
    accel_car = Car(weight_lb=300.0 + 110.0,
                    weight_dist=0.47,
                    cg_z_in=x,
                    wheels=wheels,
                    engine=engine,
                    aero=no_aero,
                    braking_g=1.36,
                    yaw_accel=15,
                    cda=2.0,
                    cla=2.0,
                    lat_g=1.36)
    try:
        return comp.get_points(car, accel_car)
    except: traceback.print_exc()

def cg_no_aero(x):
    car = Car(weight_lb=280.0 + 150.0,
              weight_dist=0.47,
              cg_z_in=x,
              wheels=wheels,
              engine=engine,
              aero=no_aero,
              braking_g=1.36,
              yaw_accel=10,
              cda=0.0,
              cla=0.0,
              lat_g=1.36)
    accel_car = Car(weight_lb=280.0 + 110.0,
                    weight_dist=0.47,
                    cg_z_in=x,
                    wheels=wheels,
                    engine=engine,
                    aero=no_aero,
                    braking_g=1.36,
                    yaw_accel=10,
                    cda=0.0,
                    cla=0.0,
                    lat_g=1.36)
    try:
        return comp.get_points(car, accel_car)
    except: traceback.print_exc()

cg_no_aero(11.7)
#plot_points(F_yaw_latg, numpy.linspace(0.5,30,4), xlabel='yaw acceleration (rad/s)', colored_by=[1.1, 1.42, 2.0], colored_by_label='lateral acceleration (g)')
#plot_points(F_cg, numpy.linspace(0.30,0.7,40), xlabel='rear weight')
#plot_points_many_y([cg_no_aero, cg_aero], numpy.linspace(7.0,16.0,8), {cg_no_aero: 'SA, 280 lbs', cg_aero: 'SA, aero, 300 lbs'},  xlabel='cg height (in)')
#xlist = numpy.linspace(0.0,4.0,4)
#ylist = numpy.linspace(0.0,4.0,4)
#contour_plot(F_cla_cda, xlist, ylist, xlabel='cla', ylabel='cda')