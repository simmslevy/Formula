function [ f_drag ] = aero_drag( v, vehicle )

    f_drag = -(0.5 .* vehicle.co_cx .* vehicle.co_rho) .* (v).^2;

end

