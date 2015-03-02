function [ lap_data ] = data_struct( lap_data, track, vehicle )   
%% Build Data Stucture

    lap_data.t          = cumsum(track.dx./lap_data.v);
    lap_data.x          = track.x;
    lap_data.crv        = track.crv;
    
%% Accelerations
    % Continuous acc_x solution, from brk and drv
    lap_data.acc_x      = lap_data.acc_x_drv;
    lap_data.acc_x( lap_data.v_braking < lap_data.v_driving) ...
                        = lap_data.acc_x_brk(lap_data.v_braking<lap_data.v_driving);
    lap_data.acc_x( lap_data.v_startfinish < lap_data.v_drivebrake ) ...
                        = lap_data.acc_x_startfinish( lap_data.v_startfinish < lap_data.v_drivebrake ); 
                    
    % Lateral Acceleration
    lap_data.acc_y      = (lap_data.v.^2).*(-lap_data.crv);

%% Engine

    lap_data.p_applied      = ( (vehicle.m_total).*(lap_data.acc_x) - aero_drag( lap_data.v, vehicle) ) .* lap_data.v /1000; %Pmot in kW 
    
    lap_data.p_mot          = lap_data.p_applied;
    lap_data.p_mot(lap_data.p_applied < 0) = 0;
    
    lap_data.r_throttle = lap_data.p_mot./vehicle.p_mot;
    
    lap_data.e_consumed     = cumsum(lap_data.p_mot.*gradient(lap_data.t)); %econsumed in kJ
    lap_data.m_fuel_cons    = vehicle.co_spec_consumption.*lap_data.e_consumed;
    
end