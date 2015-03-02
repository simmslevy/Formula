function [ acc_x_brake_max ] = acc_x_brake_max( v, vehicle )

    f_x_brake_max   = - vehicle.co_friction.*( vehicle.m_total*9.81 + aero_lift(v,vehicle) );

    acc_x_brake_max = ( f_x_brake_max  )./vehicle.m_total;

end

