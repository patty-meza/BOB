function angle_tuples = angles2tuples(angles_cell1, angles_cell2)
    % Turn the cell array of angles into the appropriate array with motor ID
    zero = deg2motor(0);
    angle_tuples = cell(length(angles_cell1), 1);
    for i = 1:length(angles_cell1)
        angle_tuples{i} = [
            ['[(11, ', num2str(zero), '),(12, ' num2str(zero), '),'],...
            ['(13, ', num2str(deg2motor(angles_cell1{i}{1})), '),(14, ' num2str(deg2motor(angles_cell1{i}{2})), '),'],...
            ['(21, ', num2str(zero), '),(22, ' num2str(zero), '),'],...
            ['(23, ', num2str(deg2motor(angles_cell2{i}{1})), '), (24, ' num2str(deg2motor(angles_cell2{i}{2})), ')],'],...
        ];
        disp(angle_tuples{i}); % Print the array
    end
end

function motor_angle = deg2motor(angle_deg)
    % Define the linear mapping between degrres and motor angle values
    motor_angle = round((angle_deg + 180) / 360 * 4095);
end