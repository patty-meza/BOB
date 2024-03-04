# Sample data
print("test")

frames = [
    [0, 0, 30, -90, 0, 20, -20, 0], # Frame 1 (Forward swing)
    [0, 20, 60, 90, 0, 20, 0, 0], # Frame 2 (Mid swing)
    [0, 20, -20, 20, 0, 0, 30, -90], # Frame 3 (Backward swing)
    [0, 20, 0, 0, 0, 20, 60, 90], # Frame 4 (Stance)
    [0, 0, 30, -90, 0, 20, -20, 0], # Frame 5 (Forward swing)
    [0, 20, 60, 90, 0, 20, 0, 0], # Frame 6 (Mid swing)
    [0, 20, -20, 20, 0, 0, 30, -90], # Frame 7 (Backward swing)
    [0, 20, 0, 0, 0, 20, 60, 90], # Frame 8 (Stance)
]

def getRawAngles():
   return frames

# Motor IDs
motor_ids = [11, 12, 13, 14, 21, 22, 23, 24]

# Angle conversion 
x1, y1 = -90, 1023
x2, y2 = 0, 2048
# Function to convert angle to position
def angle_to_position(angle):
  m = (y2-y1) / (x2 - x1) # Calculate slope
  b = y1 - m * x1  # Calculate y-intercept
  position = m * angle + b
  return int(position)

# List to store results
angle_sequence = []

# Loop through each frame
def getFrames():
  for frame in frames:
      # Create a list of tuples for the current frame
      frame_data = [(motor_id, angle_to_position(angle)) for motor_id, angle in zip(motor_ids, frame)]
      # Append the frame data to the result list
      angle_sequence.append(frame_data)
  return angle_sequence




