%% Lap Time Simulation Basics

%     load('track_Hockenheim_GP.mat')
    load('track_FSG_2013.mat')
    LapSimulation_vehicle

%% Build Working Track Variables 

    track.dx        = 0.3;
    track.xbase     = 0:track.dx:max(track.x);
    track.crv       = interp1(track.x,track.crv_filt,track.xbase,'spline');

    track.x         = track.xbase;
    
%% Parameter Variation



param_1     = 0:0.5 :2;
param_2     = 0:0.5 :2;

for ind1 = 1:length(param_1)
    for ind2 = 1:length(param_2)
       
        param_1(ind1)
        param_2(ind2)
        
        vehicle.co_cz = param_1(ind1);
        vehicle.co_cx = param_2(ind2);
        
        [v_solution, v_driving, v_braking, v_apex] = speed_profile(track,vehicle);
        
        lap_time(ind1,ind2) = max(cumsum(track.dx./v_solution))
        
    end
end

%% Sensitivities

[dt_dcx,dt_dcz] = gradient(lap_time,param_2,param_1)

figure(1)
contourf(param_2,param_1,lap_time)
title('lap Time')
ylabel('Lift Coefficient')
xlabel('Drag Coefficient')

figure(2)
subplot(2,1,1)
contourf(param_2,param_1,dt_dcx)
title('Lap Time Sensitivity to Drag')
ylabel('Lift Coefficient')
xlabel('Drag Coefficient')
subplot(2,1,2)
contourf(param_2,param_1,dt_dcz)
title('Lap Time Sensitivity to Lift')
ylabel('Lift Coefficient')
xlabel('Drag Coefficient')

efficiency_breakeven = dt_dcx./dt_dcz;

figure(3)
contourf(param_2,param_1,efficiency_breakeven)
title('Aero Break-Even')
ylabel('Lift Coefficient')
xlabel('Drag Coefficient')

