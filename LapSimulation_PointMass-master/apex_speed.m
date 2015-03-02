function [ lap_data ] = apex_speed( track, vehicle )

%% v_apex Calculation

    % Analytical solution
    v_apex = ((vehicle.m_total*9.81)./...
            ((vehicle.m_total .* abs(track.crv) ./ vehicle.co_friction) - (0.5.*vehicle.co_cz.*vehicle.co_rho))).^0.5;
        
    % Replace implausible speeds with v_max
    v_apex(vehicle.m_total.*abs(track.crv)/vehicle.co_friction < (0.5.*vehicle.co_cz.*vehicle.co_rho)) = vehicle.v_max;
    v_apex(v_apex > vehicle.v_max) = vehicle.v_max;
    
    %Output to Lap Data Structure
    lap_data.v_apex = v_apex;

end

