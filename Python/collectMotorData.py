import os
from dynamixel_sdk import *

# Control table address
ADDR_MX_TORQUE_ENABLE = 64
ADDR_MX_PRESENT_POSITION = 132
ADDR_MX_PRESENT_VELCOITY = 128
ADDR_MX_PRESENT_CURRENT = 126




# Protocol version
PROTOCOL_VERSION = 2.0

# Default setting
DXL_IDS = [11, 12, 13, 14]
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB0'

# Value for enabling/disabling the torque
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# Initialize PortHandler and PacketHandler
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

def convert_to_signed(velocity):
    if velocity > 32767:
        return velocity - 65536
    return velocity

def open_port():
  portHandler.openPort()
  # Set port baudrate
  if not portHandler.setBaudRate(BAUDRATE):
      print("Failed to change the baudrate")
      quit()

def close_port():
  portHandler.closePort()



def read_present_position(dxl_id):
  dxl_present_position, _,_ = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_MX_PRESENT_POSITION)
  return dxl_present_position

def read_present_velocity(dxl_id):
  dxl_present_velocity,_,_= packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_MX_PRESENT_VELCOITY)
  return convert_to_signed(dxl_present_velocity)

def read_present_current(dxl_id):
  dxl_present_current,_,_ = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_MX_PRESENT_CURRENT)
  return convert_to_signed(dxl_present_current)

def getMotorData(dxl_IDS):
  open_port()
  positionList,velocityList,currentList = [],[],[]
  for id in dxl_IDS:
    positionList.append(read_present_position(id))
    velocityList.append(read_present_velocity(id))
    currentList.append(read_present_current(id))
  close_port()
  return positionList,velocityList,currentList