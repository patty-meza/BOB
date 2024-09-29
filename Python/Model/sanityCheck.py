from stable_baselines3 import PPO
import numpy as np

#change depenign on what model you want to check
model = PPO.load("ppoNewRward5Mil.zip")



obs = [0.9,0.9,0.5,0.5,0.5,0.5,0.5,0.5,0.53,0.50333,0.5,0.5,0.50333,0.5,0.5,0.5,0.495,0.4985,0.4985,0.498,0.505,0.5155,0.498,0.494,0.031,-0.018,1.037]
obs = np.array(obs, dtype='float32')  
action, _ = model.predict(obs, deterministic=True)  # Predict action
print(action)
action, _ = model.predict(obs, deterministic=True)  # Predict action
print(action)
action, _ = model.predict(obs, deterministic=True)  # Predict action
print(action)
action, _ = model.predict(obs, deterministic=True)  # Predict action
print(action)
action, _ = model.predict(obs, deterministic=True)  # Predict action
print(action)