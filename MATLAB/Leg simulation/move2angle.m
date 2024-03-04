function move2angle(start_hip_angle, start_knee_angle, goal_hip_angle, goal_knee_angle, angular_velocity)
%Moves single leg from starting joint angles to goal joint angles with a specified
%angular velocity. 

% Define leg parameters
% Define leg parameters
thigh_length = 20; % Length of thigh segment [cm]
calf_length = 15; % Length of calf segment [cm]
hip_joint = [0, 0]; % Position of hip joint (x, y)
knee_joint = [0, -thigh_length]; % Position of knee joint (x, y)
foot_length = 3; % Length of foot segment [cm]

% Initialize figure

hold on;
% Initialize leg graphics objects
hip_line = line('XData', [hip_joint(1), hip_joint(1)], 'YData', [hip_joint(2), hip_joint(2)], 'Color', 'magenta', 'LineWidth', 5);
thigh_line = line('XData', [hip_joint(1), knee_joint(1)], 'YData', [hip_joint(2), knee_joint(2)], 'Color', 'magenta', 'LineWidth', 5);

knee_line = line('XData', [knee_joint(1), knee_joint(1)], 'YData', [knee_joint(2), knee_joint(2)], 'Color', 'magenta', 'LineWidth', 5);
calf_end = knee_joint + calf_length * [0, -1]; % Calculate the position of the end of the calf segment
calf_line = line('XData', [knee_joint(1), calf_end(1)], 'YData', [knee_joint(2), calf_end(2)], 'Color', 'magenta', 'LineWidth', 5);

foot_end = calf_end + foot_length * [0, -1]; % Calculate the position of the end of the foot segment
foot_line = line('XData', [calf_end(1), foot_end(1)], 'YData', [calf_end(2), foot_end(2)], 'Color', 'magenta', 'LineWidth', 3);

hip_dot = scatter(hip_joint(1), hip_joint(2), 40, 'k', 'filled'); % Black dot for hip joint
knee_dot = scatter(knee_joint(1), knee_joint(2), 40, 'k', 'filled'); % Black dot for knee joint


% Calculate angular distance to be covered
angular_distance_hip = abs(goal_hip_angle - start_hip_angle);
angular_distance_knee = abs(goal_knee_angle - start_knee_angle);

% Calculate the number of frames needed based on angular velocity
num_frames_hip = ceil(angular_distance_hip / angular_velocity);
num_frames_knee = ceil(angular_distance_knee / angular_velocity);
num_frames = max(num_frames_hip, num_frames_knee);


% Animation parameters
% Check if start and goal hip angles are the same
if start_hip_angle == goal_hip_angle
    % If they are the same, skip animation for hip joint
    hip_bend_angles = ones(1, num_frames) * start_hip_angle;
else
    % Interpolate between start and goal angles for the hip joint
    hip_bend_angles = linspace(start_hip_angle, goal_hip_angle, num_frames);
end
% Check if start and goal knee angles are the same
if start_knee_angle == goal_knee_angle
    % If they are the same, skip animation for knee joint
    knee_bend_angles = ones(1, num_frames) * start_knee_angle;
else
    % Interpolate between start and goal angles for the knee joint
    knee_bend_angles = linspace(start_knee_angle, goal_knee_angle, num_frames);
end



for t = 1:num_frames
    % Interpolate hip and knee joint angles
    hip_angle = hip_bend_angles(t)*(-1); % Interpolate hip angle
    knee_angle = (hip_bend_angles(t) + knee_bend_angles(t))*(-1); % Interpolate knee angle

    % Calculate new joint positions
    hip_end = hip_joint + thigh_length * [sind(hip_angle), -cosd(hip_angle)];
    knee_joint = hip_end;
    calf_end = knee_joint + calf_length * [sind(knee_angle), -cosd(knee_angle)];
    foot_end = calf_end - foot_length * [-cosd(knee_angle), -sind(knee_angle)]; % Foot perpendicular to the calf

    % Update graphics objects
    thigh_line.XData = [hip_joint(1), knee_joint(1)];
    thigh_line.YData = [hip_joint(2), knee_joint(2)];

    knee_dot.XData = knee_joint(1);
    knee_dot.YData = knee_joint(2);

    calf_line.XData = [knee_joint(1), calf_end(1)];
    calf_line.YData = [knee_joint(2), calf_end(2)];

    foot_line.XData = [calf_end(1), foot_end(1)];
    foot_line.YData = [calf_end(2), foot_end(2)];

    % Pause for animation
    pause(0.01);
end

% Clear the lines from the figure
delete([hip_line, thigh_line, knee_line, calf_line, foot_line, hip_dot, knee_dot]);

end