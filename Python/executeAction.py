#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dynamixel_sdk import *  # Uses Dynamixel SDK library
import random

# Control table address for velocity
ADDR_MX_GOAL_VELOCITY = 104  # Adjust based on your model
ADDR_MX_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
VELOCITY_CONTROL_MODE = 1
ADDR_MX_PRESENT_POSITION = 132
ADDR_MX_PRESENT_VELOCITY = 128

# Protocol version
PROTOCOL_VERSION = 2.0  # See which protocol version is used in the Dynamixel

# Default setting
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB0'  # Check which port is being used on your controller

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

def open_port_Execute():
  if portHandler.openPort():
      #print("Succeeded to open the port")
      pass
  else:
      print("Failed to open the port")
      quit()

  # Set port baudrate
  if not portHandler.setBaudRate(BAUDRATE):
      print("Failed to change the baudrate")
      quit()


def close_port_Execute():
  portHandler.closePort()
  """if portHandler.closePort():
      #print("Succeeded to open the port")
      pass
  else:
      print("Failed to close the port")
      quit()"""


def read_present_position(dxl_id):

  dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_MX_PRESENT_POSITION)
  return dxl_present_position

def read_present_velocity(dxl_id):
  dxl_present_velocity, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_MX_PRESENT_VELOCITY)
  return dxl_present_velocity

#returns upper and lower bounds
def bounds(id):
  if id == 14 or id == 24:
    return 3248,2048
  if id == 13 or id == 23:
    return 2500,1150
  if id == 22:
    return 2400,1700
  if id == 12:
    return 2400,1700
  if id == 21:
    return 2800,1754
  if id == 11:
     return 2335,1179

def setVelocity(id,velocity):
  upperBound,lowerBound = bounds(id)
  present_position = read_present_position(id)
  if present_position < lowerBound:
    if velocity > 0:
      return velocity
    else:
       #return 0
       return -velocity
  elif present_position > upperBound:
    if velocity < 0:  
      return velocity
    else:
       #return 0
       return -velocity
  else:
     return velocity
  

def checkPositions(ids,lowerVelBound,upperVelBound):
  for id in ids:
    upperBound,lowerBound = bounds(id)
    present_position = read_present_position(id)
    present_velocity = read_present_velocity(id)
    if present_position < lowerBound:
      if present_velocity > 0:
        return id,present_velocity
      else:
        new_velocity = random.randint(0, upperVelBound)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, id, ADDR_MX_GOAL_VELOCITY, new_velocity)
        return id,new_velocity
    elif present_position > upperBound:
      if present_velocity < 0:  
        return id,present_velocity
      else:
        new_velocity = random.randint(lowerVelBound, 0)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, id, ADDR_MX_GOAL_VELOCITY, new_velocity)
        return id,new_velocity
    else:
      return id,present_velocity


def getVelocity(id):
  #you have to expermiently determine this quanity
  timeBetweenIterations = 1.2
  upperPosBound,lowerPosBound = bounds(id)
  present_position = read_present_position(id)
  present_velocity = read_present_velocity(id)
  distToTravelUpper = (upperPosBound-present_position)*.087891 #deg
  distToTravelLower = (lowerPosBound-present_position)*.087891 #deg
  upperVelLimit = ((distToTravelUpper/timeBetweenIterations)/360)*60 #rev/sec
  lowerVelLimit = ((distToTravelLower/timeBetweenIterations)/360)*60 #rev/sec
  upperVelLimitUnitCorrected=upperVelLimit*(1/.22888)
  lowerVelLimitUnitCorrected=lowerVelLimit*(1/.22888)
  #print(upperVelLimitUnitCorrected)
  #print(lowerVelLimitUnitCorrected)
  velocity = random.randint(round(lowerVelLimitUnitCorrected), round(upperVelLimitUnitCorrected))
  return velocity




# Enable torque and set goal velocity for each Dynamixel motor
def executeMotorAction(dxl_ids,iterationPolicy,velBounds):
  lowerVelBound,upperVelBound = velBounds
  delta_velocity_list = []
  #open_port_Execute()
  for i, dxl_id in enumerate(dxl_ids):
    #print(dxl_id)
    #checkPositions(dxl_ids,lowerVelBound,upperVelBound)
    if iterationPolicy[i] == 'off':
      deltaV = 0
      _, _ = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_MX_GOAL_VELOCITY, deltaV)
      delta_velocity_list.append(deltaV)
    else:
      #delta_Velocity = random.randint(lowerVelBound, upperVelBound)
      # Set Goal Velocity
      #elocity = setVelocity(dxl_id,delta_Velocity)
      velocity = getVelocity(dxl_id)
      _, _ = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_MX_GOAL_VELOCITY, velocity)
      delta_velocity_list.append(velocity)
  #portHandler.closePort()
  #close_port_Execute()
  return delta_velocity_list

