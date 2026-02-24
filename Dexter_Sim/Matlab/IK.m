close all;
clear all;
clc;

syms theta1 theta2 theta3 theta4 theta5 theta6;

T01 = [cos(theta1) -sin(theta1) 0 0; sin(theta1) cos(theta1) 0 0; 0 0 1 0.082; 0 0 0 1];
T12 = [-sin(theta2) -cos(theta2) 0 0; 0 0 -1 0; cos(theta2) -sin(theta2) 0 0; 0 0 0 1];
T23 = [cos(theta3) -sin(theta3) 0 0.086; sin(theta3) cos(theta3) 0 0; 0 0 1 0; 0 0 0 1];
T34 = [sin(theta4) -cos(theta4) 0 0.077; -cos(theta4) sin(theta4) 0 0; 0 0 1 0; 0 0 0 1];
T45 = [cos(theta5) -sin(theta5) 0 0; 0 0 -1 -0.085; -sin(theta5) -cos(theta5) 0 0; 0 0 0 1];
T56 = [1 0 0 0; 0 1 0 0; 0 0 1 0.11; 0 0 0 1];

r = -0.086*sin(theta2)-0.077*sin(theta2+theta3)-0.195*sin(theta2+theta3+theta4);

r11 = -sin(theta1)*sin(theta5)-cos(theta1)*cos(theta5)*sin(theta2+theta3+theta4);
r12 = cos(theta1)*sin(theta2+theta3+theta4)*sin(theta5)-sin(theta1)*cos(theta5);
r13 = -cos(theta1)*cos(theta2+theta3+theta4);
px = cos(theta1)* r;
r21 = cos(theta1)*sin(theta5)-sin(theta1)*cos(theta5)*sin(theta2+theta3+theta4);
r22 = sin(theta1)*sin(theta2+theta3+theta4)*cos(theta5)+cos(theta1)*cos(theta5);
r23 = -sin(theta1)*cos(theta2+theta3+theta4);
py = sin(theta1)* r;
r31 = cos(theta5)*sin(theta2+theta3+theta4);
r32 = -sin(theta5)*cos(theta2+theta3+theta4);
r33 = sin(theta2+theta3+theta4);
pz = -0.086*cos(theta2)-0.077*cos(theta2+theta3)-0.195*cos(theta2+theta3+theta4)+0.082;

T06 = [r11 r12 r13 px; r21 r22 r23 py; r31 r32 r33 pz; 0 0 0 1];


T16 = T01\T06;
%{
disp("T16 = ");
disp(latex(simplify(T16)));
%}

T16_2 = T12*T23*T34*T45*T56;
disp("T16_2 = ");
disp(latex(simplify(T16_2)));




