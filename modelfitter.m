clf
clc
close all
load('B1464run18.mat')
Bestunc = rand(4,1);
Bestsearch = rand(4,1);
for i = 1:1:100
    Beta0 = rand(4,1);
    % seems legit  0.9597
    %    0.3404
    %   0.5853
    %  0.2238
    % Beta0 =[0.5308
    %     0.7792
    %     0.9340
    %     0.1299];
    global X Y

    X = SA(7.969*10^4+1772:7.969*10^4+2656);
    Y = FY(7.969*10^4+1772:7.969*10^4+2656);
    % ‘Beta’ is the vector corresponding to the estimated values of B, C, D, and E
    %opts = optimoptions('fminunc','Algorithm','quasi-newton');
    %xunc = fminunc(@Fsumsquares,Beta0,opts);
    xsearch = fminsearch(@Fsumsquares,Beta0);
%     if Fsumsquares(xunc)<Fsumsquares(Bestunc)
%     	Bestunc = xunc;
%     end
    if Fsumsquares(xsearch)<Fsumsquares(Bestsearch)
    	Bestsearch = xsearch;
    end

end
figure(i)
plot(X,Y,'x')
hold on
% plot(-15:.1:15,MagicFormula(Bestunc,-15:.1:15),'r')
plot(-15:.1:15,MagicFormula(Bestsearch,-15:.1:15),'c')
