function [ acc_y_max ] = acc_y_max( v, vehicle )

    f_y_max = vehicle.co_friction.*( vehicle.m_total*9.81 + aero_lift(v,vehicle) );

    acc_y_max = f_y_max./vehicle.m_total;

end

