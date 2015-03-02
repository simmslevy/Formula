function [lap_data] = speed_profile(track,vehicle)

%% Apex Speed Profile

    [ lap_data ] = apex_speed( track,vehicle );

%% Drive & Brake Profiles

    [ lap_data ] = phase_driving(lap_data, track, vehicle);
    [ lap_data ] = phase_braking(lap_data, track, vehicle);

%% Drive & Brake

    lap_data.v_drivebrake   = min(lap_data.v_driving,lap_data.v_braking);
    
%% Start Finish

    [ lap_data ] = phase_startfinish(lap_data,track,vehicle);
    
    %% Solution
    
    lap_data.v      = min( lap_data.v_drivebrake, lap_data.v_startfinish );
  
    
end