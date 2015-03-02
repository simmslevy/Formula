function [ tree ] = suspension_maker( P, plo )
% P is 5 x 2 that represnts positions of key points in ride (y,z)

% TODO: configure so any damper length can be given and function returns
% ride config

% TODO: change so that prodo is not optimized

% TODO: Finish calculating link lengths

% TODO: Figure out how it interfaces with aarm travel/write that code first

% TODO: Improve optional plotter

% TODO: Check faults

% Intialize suspension
tree.prodo = P(1,:);        % Pullrod outboard point
tree.prodi = P(2,:);        % Pullrod inboard point
tree.pivot = P(3,:);        % BLC pivot point
tree.dampb = P(4,:);        % Damper to bellcrank point
tree.dampc = P(5,:);        % Damper to chassis point

% Calculate link lengths
tree.pullrod = sqrt((tree.prodo(1)-tree.prodi(1))^2+(tree.prodo(2)-tree.prodi(2))^2);
% Check for faults

% Optional Plotter
if plo == 1
    plot(P(:,1),P(:,2))
end

end

