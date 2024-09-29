from gpiozero import MCP3008
from time import sleep

# Define the MCP3008 ADC object
r1 = MCP3008(channel=0) 
r2 = MCP3008(channel=2)  
r3 = MCP3008(channel=4)  
r4 = MCP3008(channel=6)  

try:
    while True:
        # Read the analog value from the ADC
        
        gamma = (1/0.0004885)
        p1 = r1.value * gamma
        p2 = r2.value * gamma
        p3 = r3.value * gamma
        p4 = r4.value * gamma        
        
        
        # Print the pressure reading
        #print("Pressure correct:", pressure, "Pressure Heel:", p2)
        print("p1",p1)
        print("p2",p2)
        print("p3",p3)
        print("p4",p4)
        
        
        # Adjust the sleep time according to your requirements
        sleep(1)  # Sleep for 1 second before taking the next reading

except KeyboardInterrupt:
    print("\nProgram stopped by the user")
