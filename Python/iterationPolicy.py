num_motors = 8
iterationPolicy = []
def getIterationPolicy():
    for i in range(2**num_motors):
        # Convert the number to binary, remove the "0b" prefix, and pad with zeros to ensure it has length num_motors
        binary_state = bin(i)[2:].zfill(num_motors)
        
        # Create a list of states ('on' or 'off') based on the binary representation
        motor_states = ['on' if bit == '1' else 'off' for bit in binary_state]
        iterationPolicy.append(motor_states)
        # Print the state of each motor for this combination
        #print(f"Combination {i + 1}: {motor_states}")
    return iterationPolicy
print(iterationPolicy)
"""
for i,code in enumerate(iterationPolicy):
    print("i",i)
    print("code",code)
    """