%% Vehicle Definition F3

%     vehicle.m_vehicle   = 550;                  %Vehicle Mass in (kg)
%     vehicle.m_driver    = 0;                   %Driver Mass in (kg)
%     vehicle.m_total     = vehicle.m_vehicle + vehicle.m_driver;
% 
%     vehicle.co_friction = 1.55;
%     vehicle.co_cz       = 5;
%     vehicle.co_cx       = 0.5;
%     vehicle.co_rho      = 1.2;
% 
%     vehicle.p_mot       = 185*0.733;    %Engine Power in (kW)
%     vehicle.co_spec_consumption = 183/3600;  %g/kWs
% 
%     vehicle.p_recu      = 75;           %Recu Power in (kW)
%         
%     vehicle.v_max = (vehicle.p_mot*1000./(0.5.*vehicle.co_cx.*vehicle.co_rho)).^(1/3);

%% Vehicle Definition Formula Student

    vehicle.m_vehicle   = 150;                  %Vehicle Mass in (kg)
    vehicle.m_driver    = 75;                   %Driver Mass in (kg)
    vehicle.m_total     = vehicle.m_vehicle + vehicle.m_driver;

    vehicle.co_friction = 1.5;
    vehicle.co_cz       = 0;
    vehicle.co_cx       = 0.5;
    vehicle.co_rho      = 1.225;

    vehicle.p_mot       = 40;   %Engine Power in (kW)
    vehicle.co_spec_consumption = 183/3600;  %g/kWs

    vehicle.v_max = (vehicle.p_mot*1000./(0.5.*vehicle.co_cx.*vehicle.co_rho)).^(1/3);