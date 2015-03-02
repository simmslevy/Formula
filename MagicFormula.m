function [ F ] = MagicFormula( P,X )
F = P(3).*sin(P(2).*atan((1-P(4)).*P(1).*X+P(4).*atan(P(1).*X)));   
end

