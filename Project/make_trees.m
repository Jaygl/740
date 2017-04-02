function [ M ] = make_trees(M, px, py, h)
%MAKE_TREES Summary of this function goes here
%   Detailed explanation goes here

for k = 1:length(px)
    M(px(k),py(k),1:h(k)) = 1;
end

