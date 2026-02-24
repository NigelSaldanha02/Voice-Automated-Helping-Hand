clear all;
close all;
clc;

syms theta2 theta3 theta4;

T12 = [-sin(theta2) -cos(theta2) 0 0; 0 0 -1 0; cos(theta2) -sin(theta2) 0 0; 0 0 0 1];
T23 = [cos(theta3) -sin(theta3) 0 0.086; sin(theta3) cos(theta3) 0 0; 0 0 1 0; 0 0 0 1];
T34 = [sin(theta4) -cos(theta4) 0 0.077; -cos(theta4) sin(theta4) 0 0; 0 0 1 0; 0 0 0 1];

T14 = T12*T23*T34;

disp("T14 =");
disp(latex(simplify(T14)));