function move2angle_dual_leg(start_hip_angle1, start_knee_angle1, goal_hip_angle1, goal_knee_angle1, start_hip_angle2, start_knee_angle2, goal_hip_angle2, goal_knee_angle2, angular_velocity)
%Moves two legs from starting joint angles to goal joint angles with a specified
%angular velocity. 

% Define leg parameters
thigh_length = 20; % Length of thigh segment [cm]
calf_length = 15; % Length of calf segment [cm]
foot_length = 3; % Length of foot segment [cm]

% Define initial positions for the first leg
hip_joint1 = [8, 5]; % Position of hip joint (x, y)
knee_joint1 = [8, 10-thigh_length]; % Position of knee joint (x, y)

% Define initial positions for the second leg
hip_joint2 = [-8, 0]; % Position of hip joint (x, y)
knee_joint2 = [-8, - thigh_length]; % Position of knee joint (x, y)

% Initialize figure
hold on;

% Initialize leg graphics objects for the first leg
hip_line1 = line('XData', [hip_joint1(1), hip_joint1(1)], 'YData', [hip_joint1(2), hip_joint1(2)], 'Color', 'magenta', 'LineWidth', 6);
thigh_line1 = line('XData', [hip_joint1(1), knee_joint1(1)], 'YData', [hip_joint1(2), knee_joint1(2)], 'Color', 'magenta', 'LineWidth', 6);
knee_line1 = line('XData', [knee_joint1(1), knee_joint1(1)], 'YData', [knee_joint1(2), knee_joint1(2)], 'Color', 'magenta', 'LineWidth', 6);
calf_end1 = knee_joint1 + calf_length * [0, -1]; % Calculate the position of the end of the calf segment
calf_line1 = line('XData', [knee_joint1(1), calf_end1(1)], 'YData', [knee_joint1(2), calf_end1(2)], 'Color', 'magenta', 'LineWidth', 6);
foot_end1 = calf_end1 + foot_length * [1, 0]; % Calculate the position of the end of the foot segment
foot_line1 = line('XData', [calf_end1(1), foot_end1(1)], 'YData', [calf_end1(2), foot_end1(2)], 'Color', 'magenta', 'LineWidth', 5);

hip_dot1 = scatter(hip_joint1(1), hip_joint1(2), 40, 'k', 'filled'); % Black dot for hip joint
knee_dot1 = scatter(knee_joint1(1), knee_joint1(2), 40, 'k', 'filled'); % Black dot for knee joint
foot_dot1 = scatter(calf_end1(1), calf_end1(2), 30, 'm', 'filled'); % Black dot for hip joint

% Initialize leg graphics objects for the second leg
hip_line2 = line('XData', [hip_joint2(1), hip_joint2(1)], 'YData', [hip_joint2(2), hip_joint2(2)], 'Color', 'red', 'LineWidth', 6);
thigh_line2 = line('XData', [hip_joint2(1), knee_joint2(1)], 'YData', [hip_joint2(2), knee_joint2(2)], 'Color', 'red', 'LineWidth', 6);
knee_line2 = line('XData', [knee_joint2(1), knee_joint2(1)], 'YData', [knee_joint2(2), knee_joint2(2)], 'Color', 'red', 'LineWidth', 6);
calf_end2 = knee_joint2 + calf_length * [0, -1]; % Calculate the position of the end of the calf segment
calf_line2 = line('XData', [knee_joint2(1), calf_end2(1)], 'YData', [knee_joint2(2), calf_end2(2)], 'Color', 'red', 'LineWidth', 6);
foot_end2 = calf_end2 + foot_length * [1, 0]; % Calculate the position of the end of the foot segment
foot_line2 = line('XData', [calf_end2(1), foot_end2(1)], 'YData', [calf_end2(2), foot_end2(2)], 'Color', 'red', 'LineWidth', 5);

hip_dot2 = scatter(hip_joint2(1), hip_joint2(2), 40, 'k', 'filled'); % Black dot for hip joint
knee_dot2 = scatter(knee_joint2(1), knee_joint2(2), 40, 'k', 'filled'); % Black dot for knee joint
foot_dot2 = scatter(calf_end2(1), calf_end2(2), 30, 'r', 'filled'); % Black dot for hip joint

% Calculate angular distance to be covered for both legs
angular_distance_hip1 = abs(goal_hip_angle1 - start_hip_angle1);
angular_distance_knee1 = abs(goal_knee_angle1 - start_knee_angle1);
angular_distance_hip2 = abs(goal_hip_angle2 - start_hip_angle2);
angular_distance_knee2 = abs(goal_knee_angle2 - start_knee_angle2);

% Calculate the number of frames needed based on angular velocity for both legs
num_frames_hip1 = ceil(angular_distance_hip1 / angular_velocity);
num_frames_knee1 = ceil(angular_distance_knee1 / angular_velocity);
num_frames_hip2 = ceil(angular_distance_hip2 / angular_velocity);
num_frames_knee2 = ceil(angular_distance_knee2 / angular_velocity);
num_frames1 = max(num_frames_hip1, num_frames_knee1);
num_frames2 = max(num_frames_hip2, num_frames_knee2);

% Animation parameters for the first leg
% Check if start and goal hip angles are the same for the first leg
if start_hip_angle1 == goal_hip_angle1
    % If they are the same, skip animation for hip joint
    hip_bend_angles1 = ones(1, num_frames1) * start_hip_angle1;
else
    % Interpolate between start and goal angles for the hip joint of the first leg
    hip_bend_angles1 = linspace(start_hip_angle1, goal_hip_angle1, num_frames1);
end
% Check if start and goal knee angles are the same for the first leg
if start_knee_angle1 == goal_knee_angle1
    % If they are the same, skip animation for knee joint
    knee_bend_angles1 = ones(1, num_frames1) * start_knee_angle1;
else
    % Interpolate between start and goal angles for the knee joint of the first leg
    knee_bend_angles1 = linspace(start_knee_angle1, goal_knee_angle1, num_frames1);
end


% Animation parameters for the second leg
% Check if start and goal hip angles are the same for the second leg
if start_hip_angle2 == goal_hip_angle2
    % If they are the same, skip animation for hip joint
    hip_bend_angles2 = ones(1, num_frames2) * start_hip_angle2;
else
    % Interpolate between start and goal angles for the hip joint of the second leg
    hip_bend_angles2 = linspace(start_hip_angle2, goal_hip_angle2, num_frames2);
end
% Check if start and goal knee angles are the same for the second leg
if start_knee_angle2 == goal_knee_angle2
    % If they are the same, skip animation for knee joint
    knee_bend_angles2 = ones(1, num_frames2) * start_knee_angle2;
else
    % Interpolate between start and goal angles for the knee joint of the second leg
    knee_bend_angles2 = linspace(start_knee_angle2, goal_knee_angle2, num_frames2);
end

% Run animation for both legs simultaneously
for t = 1:max(num_frames1, num_frames2)
    % Update first leg
    if t <= num_frames1
        hip_angle1 = hip_bend_angles1(t)*(-1); % Interpolate hip angle for the first leg
        knee_angle1 = (hip_bend_angles1(t) + knee_bend_angles1(t))*(-1); % Interpolate knee angle for the first leg
        hip_end1 = hip_joint1 + thigh_length * [sind(hip_angle1), -cosd(hip_angle1)];
        knee_joint1 = hip_end1;
        calf_end1 = knee_joint1 + calf_length * [sind(knee_angle1), -cosd(knee_angle1)];
        foot_end1 = calf_end1 - foot_length * [-cosd(knee_angle1), -sind(knee_angle1)]; % Foot perpendicular to the calf
    end

    % Update second leg
    if t <= num_frames2
        hip_angle2 = hip_bend_angles2(t)*(-1); % Interpolate hip angle for the second leg
        knee_angle2 = (hip_bend_angles2(t) + knee_bend_angles2(t))*(-1); % Interpolate knee angle for the second leg
        hip_end2 = hip_joint2 + thigh_length * [sind(hip_angle2), -cosd(hip_angle2)];
        knee_joint2 = hip_end2;
        calf_end2 = knee_joint2 + calf_length * [sind(knee_angle2), -cosd(knee_angle2)];
        foot_end2 = calf_end2 - foot_length * [-cosd(knee_angle2), -sind(knee_angle2)]; % Foot perpendicular to the calf
    end

    % Update graphics objects for the first leg
    if t <= num_frames1
        thigh_line1.XData = [hip_joint1(1), knee_joint1(1)];
        thigh_line1.YData = [hip_joint1(2), knee_joint1(2)];
        knee_line1.XData = [knee_joint1(1), knee_joint1(1)];
        knee_line1.YData = [knee_joint1(2), knee_joint1(2)];
        calf_line1.XData = [knee_joint1(1), calf_end1(1)];
        calf_line1.YData = [knee_joint1(2), calf_end1(2)];
        foot_line1.XData = [calf_end1(1), foot_end1(1)];
        foot_line1.YData = [calf_end1(2), foot_end1(2)];
        knee_dot1.XData = knee_joint1(1);
        knee_dot1.YData = knee_joint1(2);
        foot_dot1.XData = calf_end1(1);
        foot_dot1.YData = calf_end1(2);
    end

    % Update graphics objects for the second leg
    if t <= num_frames2
        thigh_line2.XData = [hip_joint2(1), knee_joint2(1)];
        thigh_line2.YData = [hip_joint2(2), knee_joint2(2)];
        knee_line2.XData = [knee_joint2(1), knee_joint2(1)];
        knee_line2.YData = [knee_joint2(2), knee_joint2(2)];
        calf_line2.XData = [knee_joint2(1), calf_end2(1)];
        calf_line2.YData = [knee_joint2(2), calf_end2(2)];
        foot_line2.XData = [calf_end2(1), foot_end2(1)];
        foot_line2.YData = [calf_end2(2), foot_end2(2)];
        knee_dot2.XData = knee_joint2(1);
        knee_dot2.YData = knee_joint2(2);
        foot_dot2.XData = calf_end2(1);
        foot_dot2.YData = calf_end2(2);
    end

    % Pause for animation
    pause(0.1);
end

% Clear the lines from the figure for the first leg
delete(hip_line1);
delete(thigh_line1);
delete(knee_line1);
delete(calf_line1);
delete(foot_line1);
delete(hip_dot1);
delete(knee_dot1);
delete(foot_dot1);

% Clear the lines from the figure for the second leg
delete(hip_line2);
delete(thigh_line2);
delete(knee_line2);
delete(calf_line2);
delete(foot_line2);
delete(hip_dot2);
delete(knee_dot2);
delete(foot_dot2);



end