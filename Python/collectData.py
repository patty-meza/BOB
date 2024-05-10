import csv
import time
from intilizeMotors import openPort,disableMotors_closePorts,setMotorsToIntialPosition,closeport,setMotorsToVelocityControl
from executeAction import executeMotorAction, close_port_Execute, open_port_Execute
from iterationPolicy import getIterationPolicy
from collectMotorData import getMotorData
from read_data import read_acc

csv_file_name = 'data.csv'

iterationPolicy = getIterationPolicy()
velocity_bounds = (-75,75)
#iterationPolicy = [['on','on','on','on','on','on','on','on'],['off','on','off','on','on','off','off','on']]
#iterationPolicy = [['on','on','on','off','off','on','off','off']]
iterationPolicy = [['on','on','on','on','off','off','off','off']]
#iterationPolicy = [['off','off','off','off','off','off','off','off']]
dxl_ids = [24,14,23,13,21,22,12,11]



with open(csv_file_name, mode='a', newline='') as file:
  writer = csv.writer(file)
  for i in range(10):
    for policy in iterationPolicy:

      #initilzie motors before 
      openPort()
      setMotorsToIntialPosition(dxl_ids)
      setMotorsToVelocityControl(dxl_ids)
      closeport()
      open_port_Execute()
      for i in range(150):
        start_time = time.time()
        theta,thetaDot,current = getMotorData(dxl_ids)
        acceleration = read_acc()
        #print("theta",theta)
        #print("thetaDot",thetaDot)
        #print("current",current)
        #start_time = time.time()
        action = executeMotorAction(dxl_ids,policy,velocity_bounds)

        #print("action",action)
        time.sleep(.1)
        theta_state2,thetaDot_state2,current_state2 = getMotorData(dxl_ids)
        acceleration_state2 = read_acc()
        row_data = theta + thetaDot + current + acceleration + action + theta_state2 + thetaDot_state2 + current_state2 + acceleration_state2
        writer.writerow(row_data)
        #time.sleep(.05)
        end_time = time.time()
        execution_time = end_time - start_time
        print("Execution time:", execution_time, "seconds")

      close_port_Execute()
      disableMotors_closePorts(dxl_ids)
      time.sleep(.5)


