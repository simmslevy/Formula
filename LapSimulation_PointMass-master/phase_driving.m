function [ lap_data ] = phase_driving( lap_data, track, vehicle )

    v_driving(1) = lap_data.v_apex(1);

    for ind = 1:(length(lap_data.v_apex)-1);

        dt(ind)                 = track.dx./v_driving(ind); 
        acc_x_drive_max(ind)    = acc_x_drive(v_driving(ind), track.crv(ind), vehicle); 
        
        v_temp(ind+1)   = v_driving(ind) + dt(ind).*acc_x_drive_max(ind);
        v_driving(ind+1)= min(v_temp(ind+1),lap_data.v_apex(ind+1));

    end
        acc_x_drive_max(ind+1)  = acc_x_drive(v_driving(ind+1), track.crv(ind+1), vehicle); 
    
    %% Build Lap Data Structure
    lap_data.acc_x_drv  = acc_x_drive_max;
    lap_data.acc_x_drv(v_driving == lap_data.v_apex) = 0;
    
    lap_data.v_driving  = v_driving;


end

