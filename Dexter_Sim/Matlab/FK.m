close all;
clear all;
clc;

syms theta1 theta2 theta3 theta4 theta5 theta6;

T1 = [cos(theta1) -sin(theta1) 0 0; sin(theta1) cos(theta1) 0 0; 0 0 1 0.082; 0 0 0 1];
T2 = [-sin(theta2) -cos(theta2) 0 0; 0 0 -1 0; cos(theta2) -sin(theta2) 0 0; 0 0 0 1];
T3 = [cos(theta3) -sin(theta3) 0 0.086; sin(theta3) cos(theta3) 0 0; 0 0 1 0; 0 0 0 1];
T4 = [sin(theta4) -cos(theta4) 0 0.077; -cos(theta4) sin(theta4) 0 0; 0 0 1 0; 0 0 0 1];
T5 = [cos(theta5) -sin(theta5) 0 0; 0 0 -1 -0.085; -sin(theta5) -cos(theta5) 0 0; 0 0 0 1];
T6 = [1 0 0 0; 0 1 0 0; 0 0 1 0.11; 0 0 0 1];

T06 = T1*T2*T3*T4*T5*T6;
Px = T06(1,4);
Py = T06(2,4);
Pz = T06(3,4);

%{
disp("T06 =")
disp(latex(T06));
disp("Px =");
disp(latex(Px));
disp("Py =");
disp(latex(Py));
disp("Pz =");
disp(latex(Pz));
%}

T26 = T1\T06;
T25 = T6\T26;
T24 = T5\T25;

disp("T24 =");
disp(latex(simplify(T24)));


