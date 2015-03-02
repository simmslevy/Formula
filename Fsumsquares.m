function Score = Fsumsquares(Beta)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
global X Y
Score = sum((MagicFormula(Beta,X) - Y).^2);


end

