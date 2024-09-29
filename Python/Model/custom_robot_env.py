import gym
from gym import spaces
import numpy as np
import torch
from gym.envs.registration import register
from kinematicsModel import n_features, k_labels,EnvNetwork
import random

class CustomRobotEnv(gym.Env):
    metadata = {'render.modes': ['console']}

    def __init__(self, model_path, input_size, output_size):
        super(CustomRobotEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        self.action_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=np.concatenate([np.zeros(24), -1*np.ones(3)]),
            high=np.concatenate([np.ones(24), 1.75*np.ones(3)]),
            dtype=np.float32
        )
        
        self.iteration_count = 0  # Initialize step counter
        # Load the trained MLP model
        self.model = EnvNetwork(input_size, output_size)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()  # Set the model to evaluation mode

    def seed(self, seed=None):
        pass

    def step(self, action):
        # Ensure action and current state are tensors
        action_tensor = torch.tensor([action], dtype=torch.float32)
        state_tensor = torch.tensor(self.state, dtype=torch.float32)
        action_tensor = action_tensor.squeeze()
        concat_tensor = torch.tensor([0.5, 0.5, 0.5, 0.5])
        action_tensor = torch.cat((action_tensor, concat_tensor))
        # Combine state and action
        combined_input = torch.cat((state_tensor, action_tensor))

        
        # Update iteration count
        self.iteration_count += 1

        # Get model output for next state
        with torch.no_grad():
            next_state = self.model(combined_input).numpy()

        # Compute reward and check if episode is done
        reward = self.compute_reward(next_state)
        done = self.is_done(next_state)
        
        # Update current state
        self.state = next_state
        
        # Optional: return extra info about the step
        info = {}
        
        return next_state, reward, done, info

    def reset(self):
        # Reset the state of the environment to an initial state
        randomStart = self.observation_space.sample()  # Generates a valid state respecting the observation space bounds
        standingStart = torch.tensor([0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,round(random.random(), 5),round(random.random(), 5),round(random.random(), 5),round(random.random(), 5),round(random.random(), 5),round(random.random(), 5),round(random.random(), 5),round(random.random(), 5),0.495,0.4985,0.4985,0.498,0.505,0.5155,0.498,0.494,0.0,0,1.])
        self.iteration_count = 0  # Reset iteration count
        epsilon = .7
        #with some prob epsilon either start standing with random velocity or at some complelet randmot starting point
        if random.random() > epsilon:
            self.state = randomStart
        else:
            self.state = standingStart
        return self.state


    def render(self, mode='console'):
        if mode == 'console':
            print("Current state:", self.state)

    def close(self):
        pass

    def compute_reward(self, state):
        angles = state[:8]
        velocities = state[8:16]
        current = state[16:24]

        #angle
        k1 = 10
        #current
        k2 = 10
        #acceleration
        k3 = 28/3.5

        # Angles (first 8 dimensions)
        angle_diffs = np.abs(0.5 - state[:8])
        angle_diffs_sum =np.sum(angle_diffs)
        angle_reward = (angle_diffs_sum * k1)**2
        

        # Currents (indices 16 to 23)
        current_diffs = np.abs(0.5 - state[16:24])
        current_reward = np.sum(current_diffs) * k2

        # Accelerations (last 3 dimensions)
        # Calculate absolute differences
        acceleration_diffs = np.abs(state[24:27])

        # Modify the differences for specific elements
        acceleration_diffs[0] = np.abs(0 - state[24])
        acceleration_diffs[1] = np.abs(0 - state[25])
        acceleration_diffs[2] = np.abs(1 - state[26])

        # Sum all the modified absolute differences
        acceleration_diffs = np.sum(acceleration_diffs)
        acceleration_reward = (np.sum(acceleration_diffs) * k3) 

        # Calculate total reward
        #print("angle",angle_diffs_sum, angle_reward)
        #print("current",np.sum(current_diffs),current_reward)
        #print("acceleartion",acceleration_diffs,acceleration_reward**2)
        #print("difference ", angle_reward-(acceleration_reward**2))
        return -(angle_reward + current_reward + acceleration_reward**2)
        if angle_diffs_sum > 1:
            total_reward = -(angle_reward*2 + current_reward + acceleration_reward)
        else:
            total_reward = -(angle_reward + current_reward + acceleration_reward**2)

        return total_reward

    def is_done(self, state):
        # End the episode after 1000 iterations
        # Modify the differences for specific elements
        accelerationX = state[24]
        accelerationY = state[25]
        accelerationZ = state[26]
        #print("x ",accelerationX)
        #print("y ",accelerationY)
        #print("z ",accelerationZ)
        #if self.iteration_count >=10:
        #    if accelerationX > .7 or accelerationY > .7 or accelerationX < -.7 or accelerationY <-.7:
        #        return True
        return self.iteration_count >= 50

# Load your trained MLP model
model_path = 'env_network.pth'
input_size = n_features  # Example input size
output_size = k_labels  # Example output size


# Define the ID for your custom environment
env_id = 'BobModel'

# Register your custom environment with Gym

gym.register(
    id='BobModel',
    entry_point='custom_robot_env:CustomRobotEnv',  
    kwargs={'model_path': 'env_network.pth', 'input_size': n_features, 'output_size': k_labels}  
)



