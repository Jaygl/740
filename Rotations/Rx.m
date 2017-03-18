function [ u ] = Rx( v, theta )
%RX Summary of this function goes here
%   Detailed explanation goes here

R = [1 0 0; 0 cosd(theta) -sind(theta); 0 sind(theta) cosd(theta)];
u = R*v';

end

