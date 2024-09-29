import torch
import gym
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os
from custom_robot_env import CustomRobotEnv,n_features,k_labels

class PolicyNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 256)
        self.fc2 = nn.Linear(256, 256)
        self.mu = nn.Linear(256, output_dim)
        self.sigma = nn.Linear(256, output_dim)
        self.relu = nn.ReLU()
        self.softplus = nn.Softplus()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        mu = self.mu(x)
        sigma = self.softplus(self.sigma(x))  # Ensure sigma is positive
        mu = self.sigmoid(mu)  # Apply sigmoid activation
        return mu, sigma

class PPOAgent:
    def __init__(self, state_dim, action_dim, input_dim, lr=1e-2, gamma=0.95, clip_ratio=0.2, epochs=10):
        self.policy = PolicyNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)
        self.gamma = gamma
        self.clip_ratio = clip_ratio
        self.epochs = epochs
        self.state_dim = state_dim

    def select_action(self, state):
        state = torch.FloatTensor(state).view(1, -1)  # Reshape to 1x27
        mu, sigma = self.policy(state)
        action_dist = torch.distributions.Normal(mu, sigma)
        action = action_dist.sample()
        log_prob = action_dist.log_prob(action)
        return action.detach().numpy(), log_prob

    def update_policy(self, states, actions, log_probs, advantages):
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        log_probs = torch.stack(log_probs)
        advantages = torch.FloatTensor(advantages)

        for _ in range(self.epochs):
            mu, sigma = self.policy(states)
            action_dist = torch.distributions.Normal(mu, sigma)
            new_log_probs = action_dist.log_prob(actions)

            ratio = torch.exp(new_log_probs - log_probs)
            clipped_ratio = torch.clamp(ratio, 1 - self.clip_ratio, 1 + self.clip_ratio)
            surrogate1 = ratio * advantages
            surrogate2 = clipped_ratio * advantages
            surrogate_loss = -torch.min(surrogate1, surrogate2).mean()

            self.optimizer.zero_grad()
            surrogate_loss.backward()
            self.optimizer.step()

# Use your custom environment
env = CustomRobotEnv(model_path='env_network.pth', input_size=n_features, output_size=k_labels)


state_dim = env.observation_space.shape[0]
action_dim = env.action_space.shape[0]
action_dim = 4
print("Shape of action space:", env.action_space.shape)
print("Dimension of action space:", action_dim)
# Modify the initialization of PPOAgent
agent = PPOAgent(state_dim, action_dim, n_features)

num_episodes =10000
max_steps_per_episode = 1000
save_interval = 1000  # Save the model every 100 episodes
checkpoint_dir = 'checkpoints'

if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

for i in range(num_episodes):
    state = env.reset()
    total_reward = 0
    for _ in range(max_steps_per_episode):
        action, log_prob = agent.select_action(state)
        print(action)
        #print(np.concatenate((action, np.full((1, 4), .5)), axis=1))
        action = np.concatenate((action, np.full((1, 4), .5)), axis=1)
        print(action)
        state, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            break

    print(f"Episode {i+1}, Total Reward: {total_reward}")

    # Save the model every save_interval episodes
    if (i + 1) % save_interval == 0:
        checkpoint_path = os.path.join(checkpoint_dir, f'policy_network_episode_{i+1}.pth')
        torch.save(agent.policy.state_dict(), checkpoint_path)

env.close()
