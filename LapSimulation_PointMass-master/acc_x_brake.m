function [ acc_x_brake ] = acc_x_brake( v, crv, vehicle )

    acc_y = abs(crv).*(v).^2;

    acc_x_brake_lim = acc_x_brake_max(v,vehicle).*realsqrt(abs(1-( acc_y./acc_y_max(v,vehicle) ).^2 ));

    f_drag          = aero_drag(v,vehicle);
    acc_drag        = f_drag./vehicle.m_total;

    acc_x_brake     = acc_x_brake_lim + acc_drag;

end

