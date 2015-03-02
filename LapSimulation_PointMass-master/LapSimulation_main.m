%% Lap Time Simulation Initialize Parameters

    LapSimulation_vehicle
    LapSimulation_track

%% Speed Profile & Lap Time

    [lap_data]  = speed_profile(track,vehicle); 
    
%% Post Processing

    [lap_data] = data_struct(lap_data, track, vehicle);
    lap_time    = max(lap_data.t); 
    [ drive_point_indices, brake_point_indices ] = drive_brake_points( lap_data );
    
%% Plot Results

    LapSimulation_plot