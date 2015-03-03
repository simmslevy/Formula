function [ tree ] = suspension_maker( P, rod_type, plo )
% Work
% ALT: configure so any damper length can be given and function returns
% ride config
% TODO: Calculate Bump & Ride
% TODO: Finish calculating link lengths
% TODO: Figure out how it interfaces with aarm travel/write that code first
% TODO: Improve optional plotter
% TODO: Check faults
% TODO: Calculate end damper position


% P is 7 x 2 that represnts positions of key points in ride (y,z) for aarms


% Intialize suspension
tree.uoarm = P(1,:);        % Upper outer A-arm
tree.loarm = P(2,:);        % Lower outer A-arm
tree.uiarm = P(3,:);        % Upper inner A-arm
tree.liarm = P(4,:);        % Lower inner A-arm

% Pick prodo based on rod type
if strcmp('Pullrod',rod_type);
    tree.prodo = tree.uoarm-[1.5,1.5];        % Prod outboard point
elseif strcmp('Bottom Pushrod',rod_type);
    tree.prodo = tree.loarm-[1.5,-1.5];
elseif strcmp('Top Pushrod',rod_type);
    tree.prodo = tree.uoarm-[1.5,-1.5];
end

% Intialize the rest of the bellcrank
tree.prodi = P(5,:);        % Prod inboard point
tree.pivot = P(6,:);        % BLC pivot point
tree.dampb = P(7,:);        % Damper to bellcrank point

% Find Bump and Ride positions

% Calculate acceptable damper position
tree.dampc = calculation;        % Damper to chassis point

% Calculate link lengths
tree.pullrod = sqrt((tree.prodo(1)-tree.prodi(1))^2+(tree.prodo(2)-tree.prodi(2))^2);
% Check for faults

% Optional Plotter
if plo == 1
    plot(P(:,1),P(:,2))
end

end

