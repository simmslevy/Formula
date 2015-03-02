
function [ drive_point_indices, brake_point_indices ] = drive_brake_points( lap_data )

%% Identify Brake & Throttle Points

    index = 1:length(lap_data.p_applied);
    power_spline = spline(index,lap_data.p_applied); 

    drive_brake_transitions =fnzeros(power_spline);
    drive_brake_transitions=floor(drive_brake_transitions(1,:));

    v_transition    = lap_data.v(drive_brake_transitions);
    v_preceding     = lap_data.v(drive_brake_transitions - 1);

    brake_point_indices    = drive_brake_transitions(v_preceding < v_transition);
    drive_point_indices    = drive_brake_transitions(v_preceding > v_transition);
    drive_point_indices    = [1, drive_point_indices];



end

