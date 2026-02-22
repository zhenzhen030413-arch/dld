%Fitting Bolt Torque Data

% This script fits bolt torque data from internal and external bolts over time.

% Sample data (time in hours, torque in Nm)
time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
internal_bolt_torque = [20, 25, 30, 35, 40, 42, 43, 45, 48, 50, 55];
extternal_bolt_torque = [18, 22, 27, 33, 36, 39, 40, 42, 46, 49, 52];

% Fit a polynomial to the data
internal_fit = polyfit(time, internal_bolt_torque, 2);
extternal_fit = polyfit(time, external_bolt_torque, 2);

% Evaluate the fit
internal_fit_values = polyval(internal_fit, time);
extternal_fit_values = polyval(external_fit, time);

% Plotting the results
figure;
plot(time, internal_bolt_torque, 'ro', 'DisplayName', 'Internal Bolt Torque');
hold on;
plot(time, external_bolt_torque, 'bo', 'DisplayName', 'External Bolt Torque');
plot(time, internal_fit_values, 'r-', 'DisplayName', 'Internal Fit');
plot(time, external_fit_values, 'b-', 'DisplayName', 'External Fit');
hold off;
legend show;
title('Bolt Torque Fitting Over Time');
xlabel('Time (hours)');
ylabel('Torque (Nm)');
grid on;
