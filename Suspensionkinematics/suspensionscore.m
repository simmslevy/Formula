function score  = suspensionscore( P,w )
% Score Function Work
% Add: Merge Matt Lee Linearity Function
% Add: Aarm roll camber function
% Add: Aarm bump camber function
% Add: Roll center movement function
% Add: Damper Reaction Forces
% Add: BLC Reaction Forces
% Add: BLC Pivot Tab Length
% Add: Damper Tab Length
% Confirm: All needed penalties

BLCL = 0;                        % Linearity of Bellcranks
ARC = 0;                         % Roll Camber of Aarms
ABC = 0;                         % Bump Camber of Aarms
RM = 0;                          % Roll Center Migration
DR = 0;                          % Damper Reaction Forces
BLCPR = 0;                       % BLC Reaction Forces
BLCPMA = 0;                      % BLC Pivot Tab Length
DMA = 0;                         % Damper Tab Length



score = w(1)*BLCL^2 + w(2)*ARC^2 + w(3)*ABC^2 + w(4)*RM^2 + w(5)*DR^2 + w(6)*BLCPR^2 + w(7)*BLCPMA^2 + w(8)*DMA^2;

end

