function [ tree ] = suspension_maker( P, rod_type, plo )
% P is 4 x 2 that represnts positions of key points in ride (y,z) for aarms
tree.uoarm = P(1,:);        % Upper outer A-arm
tree.loarm = P(2,:);        % Lower outer A-arm
tree.uiarm = P(3,:);        % Upper inner A-arm
tree.liarm = P(4,:);        % Lower inner A-arm
if rod_type == 'Pullrod'
    tree.prodo = tree.uoarm-(1.5,1.5);        % Prod outboard point
elseif rod_type = 'Bottom Pushrod'
     tree.prodo = tree.loarm-(1.5,-1.5);
elseif rod_type = 'Top Pushrod'
    tree.prodo = tree.uoarm-(1.5,-1.5);
end
% TODO: make P the right size

% TODO: configure so any damper length can be given and function returns
% ride config

% TODO: change so that prodo is not optimized

% TODO: Finish calculating link lengths

% TODO: Figure out how it interfaces with aarm travel/write that code first

% TODO: Improve optional plotter

% TODO: Check faults

% TODO: Adjust bellcranks

% Intialize suspension
tree.prodo = P(1,:);        % Prod outboard point
tree.prodi = P(2,:);        % Prod inboard point
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

