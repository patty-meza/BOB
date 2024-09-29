import pandas as pd

# Load the CSV file assuming the first row is not the header if that's the case
df = pd.read_csv('data3.csv', header=None)  # Use header=None if there's no header


# Define the column indices for each data type
angle_columns = [i - 1 for i in list(range(1, 9)) + list(range(36, 44))]
velocity_columns = [i - 1 for i in list(range(9, 17)) + list(range(28, 36)) + list(range(44, 52))]
current_columns = [i - 1 for i in list(range(17, 25)) + list(range(52, 60))]
acceleration_columns = [i - 1 for i in list(range(25, 28)) + list(range(60, 63))]

# Extract data for each type based on column indices
angle_data = df.iloc[:, angle_columns]
velocity_data = df.iloc[:, velocity_columns]
current_data = df.iloc[:, current_columns]
acceleration_data = df.iloc[:, acceleration_columns]

# Manual normalization parameters
min_angle = 1000
max_angle = 3250
min_velocity = -85
max_velocity = 85
min_current = -1000
max_current = 1000

# Normalize and round the data
df.iloc[:, angle_columns] = ((angle_data - min_angle) / (max_angle - min_angle)).round(5)
df.iloc[:, velocity_columns] = ((velocity_data - min_velocity) / (max_velocity - min_velocity)).round(5)
df.iloc[:, current_columns] = ((current_data - min_current) / (max_current - min_current)).round(5)

# Save the normalized DataFrame back to a CSV without the index and with headers
df.to_csv('normalized_data3.csv', index=False)
