import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the data from the CSV file
data = pd.read_csv("data.csv")

# Define the columns for different types of data
angle_columns = list(range(1, 9)) + list(range(36, 44))
velocity_columns = list(range(9, 17)) + list(range(28, 36)) + list(range(44, 52))
current_columns = list(range(17, 25)) + list(range(52, 60))

# Normalize angles
angle_scaler = MinMaxScaler(feature_range=(1000, 3250))
data.iloc[:, angle_columns] = angle_scaler.fit_transform(data.iloc[:, angle_columns])

# Normalize velocities
velocity_scaler = MinMaxScaler(feature_range=(-150, 150))
data.iloc[:, velocity_columns] = velocity_scaler.fit_transform(data.iloc[:, velocity_columns])

# Normalize currents
current_scaler = MinMaxScaler(feature_range=(-1000, 1000))
data.iloc[:, current_columns] = current_scaler.fit_transform(data.iloc[:, current_columns])

# Save the normalized data to a new CSV file
data.to_csv("normalized_data.csv", index=False)
