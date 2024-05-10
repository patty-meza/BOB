#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dynamixel_sdk import *  # Uses Dynamixel SDK library
import time
import random

# Control table address for velocity
ADDR_MX_GOAL_VELOCITY = 104  # Adjust based on your model
ADDR_MX_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
VELOCITY_CONTROL_MODE = 1
POSITION_CONTROL_MODE = 3
ADDR_MX_PRESENT_POSITION = 132
ADDR_MX_GOAL_POSITION = 116

# Protocol version
PROTOCOL_VERSION = 2.0  # See which protocol version is used in the Dynamixel

# Default setting
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB0'  # Check which port is being used on your controller
TORQUE_ENABLE = 1     # Value for enabling the torque
TORQUE_DISABLE = 0    # Value for disabling the torque

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)



def openPort():
  # Open port
  if portHandler.openPort():
      print("Succeeded to open the port")
  else:
      print("Failed to open the port")
      quit()

  # Set port baudrate
  if not portHandler.setBaudRate(BAUDRATE):
      print("Failed to change the baudrate")
      quit()


def disableMotors(dxl_ids):
  # Disable Dynamixel Torque
  for dxl_id in dxl_ids:
      dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
      if dxl_comm_result != COMM_SUCCESS:
          print("Failed to disable torque for DXL ID %d" % dxl_id)
      elif dxl_error != 0:
          print("Error occurred while disabling torque for DXL ID %d" % dxl_id)


def setMotorsToVelocityControl(dxl_ids):
  #disable motor torque to be able to change control mode
  disableMotors(dxl_ids)
  #Enable Torques and set to velcoity control
  for i, dxl_id in enumerate(dxl_ids):
    
    # Set to Velocity Control Mode
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_OPERATING_MODE, VELOCITY_CONTROL_MODE)
    if dxl_comm_result != COMM_SUCCESS or dxl_error != 0:
        print(f"Failed to set velocity control mode for DXL ID {dxl_id}")
        continue  # Skip this motor if there's an error
    # Enable Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("Failed to enable torque for DXL ID %d" % dxl_id)
    elif dxl_error != 0:
        print("Error occurred while enabling torque for DXL ID %d" % dxl_id)
    else:
        print("Torque has been successfully enabled for DXL ID %d" % dxl_id)

def second_digit(number):
    return number % 10

def setMotorsToIntialPosition(dxl_ids):
  #disable motors to be able to change operating mode
  disableMotors(dxl_ids)
  # Sorting the numbers based on the units place
  dxl_ids = sorted(dxl_ids, key=second_digit)
  #Enable Torques and set to Position control
  for i, dxl_id in enumerate(dxl_ids):
    
    # Set to Position Control Mode
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_OPERATING_MODE, POSITION_CONTROL_MODE)
    if dxl_comm_result != COMM_SUCCESS or dxl_error != 0:
        print(f"Failed to set velocity control mode for DXL ID {dxl_id}")
        continue  # Skip this motor if there's an error
    

    # Enable Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_MX_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("Failed to enable torque for DXL ID %d" % dxl_id)
    elif dxl_error != 0:
        print("Error occurred while enabling torque for DXL ID %d" % dxl_id)
    else:
        print("Torque has been successfully enabled for DXL ID %d" % dxl_id)
    
    #set motor to intial Position
    goal_position = 2048
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_MX_GOAL_POSITION, goal_position)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to send goal position to motor ID {dxl_id}: {packetHandler.getTxRxResult(dxl_comm_result)}")
        portHandler.closePort()
        return False
    time.sleep(.5)
  time.sleep(1)
  disableMotors(dxl_ids)




# Close port
def closeport():
  portHandler.closePort()

def disableMotors_closePorts(dxl_ids):
  
    openPort()
    # Disable Dynamixel Torque
    for dxl_id in dxl_ids:
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, dxl_id, ADDR_MX_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to disable torque for DXL ID %d" % dxl_id)
        elif dxl_error != 0:
            print("Error occurred while disabling torque for DXL ID %d" % dxl_id)
    closeport()