function [ acc_x_drive ] = acc_x_drive( v, crv, vehicle )

    acc_y = abs(crv).*(v).^2;

    acc_x_drive_lim = acc_x_drive_max(v,vehicle).*realsqrt(abs(1-( acc_y./acc_y_max(v,vehicle) ).^2));

    %% Engine

    acc_engine      = vehicle.p_mot*1000./v./vehicle.m_total;
    acc_x_drive_lim     = min(acc_engine,acc_x_drive_lim);

    %% Drag

    f_drag          = aero_drag(v,vehicle);
    acc_drag        = f_drag./vehicle.m_total;

    acc_x_drive     = acc_x_drive_lim + acc_drag;

end

