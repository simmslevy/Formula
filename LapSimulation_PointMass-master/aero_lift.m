function [ f_lift ] = aero_lift( v, vehicle )

    f_lift = (0.5 .* vehicle.co_cz .* vehicle.co_rho) .* (v).^2;

end

