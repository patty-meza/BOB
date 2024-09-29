import pandas as pd
from sklearn.model_selection import train_test_split
import torch
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
import numpy as np

# Load the CSV file
data = pd.read_csv('dataCleaning/normalized_data3.csv')

# Define column indices according to the provided structure
angle_columns = [i - 1 for i in list(range(1, 9)) + list(range(36, 44))]
velocity_columns = [i - 1 for i in list(range(9, 17)) + list(range(28, 36)) + list(range(44, 52))]
current_columns = [i - 1 for i in list(range(17, 25)) + list(range(52, 60))]
acceleration_columns = [i - 1 for i in list(range(25, 28)) + list(range(60, 63))]

# Extract features and labels
features = data.iloc[:, angle_columns[:8] + velocity_columns[:8] + current_columns[:8] + acceleration_columns[:3] + velocity_columns[8:16]]
labels = data.iloc[:, angle_columns[8:] + velocity_columns[16:] + current_columns[8:] + acceleration_columns[3:]]

# Split data into training, validation, and test sets
train_val_features, test_features, train_val_labels, test_labels = train_test_split(features, labels, test_size=0.2, random_state=42)
train_features, val_features, train_labels, val_labels = train_test_split(train_val_features, train_val_labels, test_size=0.25, random_state=42)  # 0.25 x 0.8 = 0.2

# Convert to torch tensors
train_features = torch.tensor(train_features.values, dtype=torch.float32)
train_labels = torch.tensor(train_labels.values, dtype=torch.float32)
val_features = torch.tensor(val_features.values, dtype=torch.float32)
val_labels = torch.tensor(val_labels.values, dtype=torch.float32)
test_features = torch.tensor(test_features.values, dtype=torch.float32)
test_labels = torch.tensor(test_labels.values, dtype=torch.float32)

# Create DataLoaders
train_data = TensorDataset(train_features, train_labels)
train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_data = TensorDataset(val_features, val_labels)
val_loader = DataLoader(val_data, batch_size=32, shuffle=True)

# Define the neural network class
class EnvNetwork(nn.Module):
    def __init__(self, n_features, k_labels):
        super(EnvNetwork, self).__init__()
        self.fc1 = nn.Linear(n_features, 256)
        self.fc2 = nn.Linear(256, 256)
        self.fc3 = nn.Linear(256, k_labels)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)

# Initialize network, loss, and optimizer
n_features = train_features.shape[1]
k_labels = train_labels.shape[1]
model = EnvNetwork(n_features, k_labels)
criterion = nn.MSELoss()  # Use Mean Squared Error for regression tasks
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 100
for epoch in range(num_epochs):
    model.train()
    train_loss = 0
    for features, labels in train_loader:
        optimizer.zero_grad()
        output = model(features)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
        train_loss += loss.item()

    # Validation phase
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for features, labels in val_loader:
            output = model(features)
            loss = criterion(output, labels)
            val_loss += loss.item()

    print(f"Epoch {epoch+1}/{num_epochs}, Training Loss: {train_loss/len(train_loader):.4f}, Validation Loss: {val_loss/len(val_loader):.4f}")

# Evaluate on test set
model.eval()
test_loss = 0
with torch.no_grad():
    for features, labels in DataLoader(TensorDataset(test_features, test_labels), batch_size=32):
        #print(features)
        output = model(features)
        loss = criterion(output, labels)
        test_loss += loss.item()

print(f"Test Loss: {test_loss/len(test_features):.4f}")

# Save the trained model
torch.save(model.state_dict(), 'env_network.pth')

"""
custom_vector = np.array([0.46711,0.46667,0.46622,0.46622,0.43911,0.476,0.464,0.46578,0.53,0.50333,0.5,0.5,0.50333,0.5,0.5,0.5,0.495,0.4985,0.4985,0.498,0.505,0.5155,0.498,0.494,0.031,-0.018,1.037,0,0,0,0,0.5,0.5,0.5,0.5])  # Your custom vector values

# Preprocess the custom vector (assuming the same preprocessing as your training data)
# For example, you might need to normalize the vector
# custom_vector = (custom_vector - mean) / std  # Normalize if needed

# Convert the custom vector to a PyTorch tensor
custom_tensor = torch.tensor(custom_vector, dtype=torch.float32)

# Reshape the tensor if necessary (depends on the shape expected by your model)
# custom_tensor = custom_tensor.reshape(1, -1)  # Reshape if needed

# Pass the tensor through the model to get predictions
with torch.no_grad():
    model.eval()  # Set the model to evaluation mode
    output = model(custom_tensor)

# Output will be the predictions made by your model on the custom input vector
print("Predictions:", output)

"""