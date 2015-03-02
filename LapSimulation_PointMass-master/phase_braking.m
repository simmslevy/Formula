function [ lap_data ] = phase_braking( lap_data, track, vehicle )

    v_braking(length(lap_data.v_apex)) = lap_data.v_apex(length(lap_data.v_apex));

    for ind = length(lap_data.v_apex):-1:2;

        dt(ind)         = track.dx./v_braking(ind);
        acc_x_brake_max(ind)      = acc_x_brake(v_braking(ind), track.crv(ind), vehicle); 
        
        v_temp(ind-1)   = v_braking(ind) - dt(ind).*acc_x_brake_max(ind);
        v_braking(ind-1)  = min(v_temp(ind-1),lap_data.v_apex(ind-1));

    end
    
        acc_x_brake_max(ind-1)      = acc_x_brake(v_braking(ind-1), track.crv(ind-1), vehicle); 

    %% Build Lap Data Structure
    lap_data.acc_x_brk  = acc_x_brake_max;
    lap_data.acc_x_brk(v_braking == lap_data.v_apex) = 0;
    
    lap_data.v_braking  = v_braking;
    
end

