function [ acc_x_drive_max ] = acc_x_drive_max( v, vehicle )

    f_x_drive_max   = vehicle.co_friction.*( vehicle.m_total*9.81 + aero_lift(v,vehicle) );

    acc_x_drive_max = ( f_x_drive_max )./vehicle.m_total;      %f_drag negative

end

