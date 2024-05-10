function angle_deg = motor2deg(motor_angle)
    % Define the linear mapping between motor angle values and degree
    angle_deg = (motor_angle / 4095) * 360 - 180;
end

