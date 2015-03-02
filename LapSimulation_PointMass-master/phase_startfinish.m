function [ lap_data ] = phase_startfinish( lap_data, track, vehicle )

%% Initialize Acceleration Vector

lap_data.v_startfinish   = 999*ones(1,length(lap_data.v_drivebrake));
acc_startfinish = zeros(1,length(lap_data.v_drivebrake));

%%
switch lap_data.v_drivebrake(1) > lap_data.v_drivebrake(end)  
%% Accelerate across StartFinish    
    case 1       
        
        dt                          = track.dx./lap_data.v_drivebrake;
        lap_data.v_startfinish(1)   = lap_data.v_drivebrake(end) + dt(end).*acc_x_drive(lap_data.v_drivebrake(end), track.crv(end), vehicle); 
        
        for ind = 1:length(lap_data.v_drivebrake);
            
            dt(ind)                 = track.dx./lap_data.v_startfinish(ind);  
            acc_startfinish(ind)    = acc_x_drive(lap_data.v_startfinish(ind), track.crv(ind), vehicle);
            
            v_temp(ind+1)           = lap_data.v_startfinish(ind) + dt(ind).*acc_startfinish(ind);

            if v_temp(ind+1) > lap_data.v_drivebrake(ind+1)
            break
            end

            lap_data.v_startfinish(ind+1)  = min(v_temp(ind+1),lap_data.v_drivebrake(ind+1));       
        end
        
%% Brake across StartFinish 
    case 0      
        
        dt                  = track.dx./lap_data.v_drivebrake;
        lap_data.v_startfinish(end)   = lap_data.v_drivebrake(1) - dt(1).*acc_x_brake(lap_data.v_drivebrake(1), track.crv(1), vehicle); 
     
        for ind = length(lap_data.v_drivebrake):-1:2;
            
            dt(ind)         = track.dx./lap_data.v_startfinish(ind);
            acc_startfinish(ind) = acc_x_brake(lap_data.v_startfinish(ind), track.crv(ind), vehicle);
            
            v_temp(ind-1)   = lap_data.v_startfinish(ind) - dt(ind).*acc_startfinish(ind);

            if v_temp(ind-1) > lap_data.v_drivebrake(ind-1)
            break
            end

            lap_data.v_startfinish(ind-1)  = min(v_temp(ind-1),lap_data.v_drivebrake(ind-1));            
        end
end

    %Write Accel Data to 
    lap_data.acc_x_startfinish = acc_startfinish;


end

