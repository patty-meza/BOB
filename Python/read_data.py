import time
from icm20948 import ICM20948
from gpiozero import MCP3008


def normalize_pressure_sensor(voltage):
    ## min val = 0.0004, max val = 6.0
    normalized_value = ((voltage) - 0.0004) / (6.0 - 0.0004)  
    # Constrain the normalized value between 0 and 1
    ##normalized_value = max(0, min(normalized_value, 1))
    return normalized_value

def read_acc():
    """
    Read accelerometer data.
    Returns:
    - accelerometer readings (ax, ay, az) [gs]
    """
    imu = ICM20948() ## create IMU object
    imu.set_accelerometer_low_pass(enabled=True, mode=5)
   
    ############ IMU READINGS ##########
    ax, ay, az, gx_raw, gy_raw, gz_raw = imu.read_accelerometer_gyro_data() # Read raw IMU data 
    ## accelerometer is in units of gs (sitting flat on table: az = 1, freefall: az = 0)

    # Print IMU data
    ax = round(ax, 3)
    ay = round(ay,3)
    az = round(az,3)
    acceleration_list = [ax,ay,az]
    #print("Acc X:", ax, "Acc Y:", ay, "Acc Z:", az)
    return acceleration_list

def read_all_sensors(prev_time, prev_gyro):
    """
    Read accelerometer, gyroscope, and pressure sensor data.
    
    Args:
    - prev_time: last time the function was called
    - prev_gyro: Tuple containing previous accelerometer readings (gx, gy, gz)

    Returns:
    - Tuple containing current accelerometer readings (ax, ay, az) [gs]
    - Tuple containing current gyroscope readings (gx, gy, gz) [degrees]
    - Tuple containing current pressure sensor readings (toe_pressure_1, toe_pressure_2, heel_pressure_1, heel_pressure_2)
    """
    imu.set_accelerometer_low_pass(enabled=True, mode=5)
    imu.set_gyro_low_pass(enabled=True, mode=5)
    
    data_time = time.time() #[seconds]
    dt = prev_time - data_time

    imu = ICM20948() ## create IMU object
    # Create separate MCP3008 objects for each pressure sensor
    adc_sensor1 = MCP3008(channel=0, device=0)  # Channel 0
    adc_sensor2 = MCP3008(channel=2, device=0)  # Channel 2
    adc_sensor3 = MCP3008(channel=4, device=0)  # Channel 4
    adc_sensor4 = MCP3008(channel=6, device=0)  # Channel 6

    ###### Read voltage from each pressure sensor and calculate ADC value ######
    # normalize pressure sensor vals [0,1]
    toe_pressure_1 = normalize_pressure_sensor(adc_sensor1.value)
    toe_pressure_2 = normalize_pressure_sensor(adc_sensor2.value)
    heel_pressure_1 = normalize_pressure_sensor(adc_sensor3.value)
    heel_pressure_2 = normalize_pressure_sensor(adc_sensor4.value)

    ############ IMU READINGS ##########
    ax, ay, az, gx_raw, gy_raw, gz_raw = imu.read_accelerometer_gyro_data() # Read raw IMU data 
    ## accelerometer is in units of gs (sitting flat on table: az = 1, freefall: az = 0)
  
    gx = (prev_gyro[0] + gx_raw * dt)/360    ## gyroscope is in degrees (div by 360 to normalize)
    gy = (prev_gyro[1] + gy_raw * dt)/360
    gz = (prev_gyro[2] + gz_raw * dt)/360
    ## reset to zero for +- 360 degrees (or 1 since its mapped) this uses modulo operator
    gx %= 1
    gy %= 1
    gz %= 1

    ## update input variables
    prev_time = data_time
    prev_gyro = (gx, gy, gz)

    # Print IMU data
    print("Acc X:", round(ax, 3), "Acc Y:", round(ay,3), "Acc Z:", round(az,3), "Gyr X:", round(gx,3), "Gyr Y:", round(gy,3), "Gyr Z:", round(gz,3))
    # Print pressure sensor data
    print("P1:", round(toe_pressure_1,3), "P2:", round(toe_pressure_2,3), "P3:", round(heel_pressure_1,3), "P4:", round(heel_pressure_2,3))

    return data_time, (ax, ay, az), (gx, gy, gz), (toe_pressure_1, toe_pressure_2, heel_pressure_1, heel_pressure_2)

# # Initialize 
# prev_gyro = (0, 0, 0)
# prev_time = time.time()

# # Call the read_all_sensors function 100 times in a loop
# for _ in range(100):
#     read_all_sensors(prev_time, prev_gyro)
#     time.sleep(0.1)  # Add a delay of 1 second between each call

### Test accelerometer
"""
for _ in range(100):
    read_acc()
    time.sleep(0.01)  # Add a delay of 1 second between each call
    """