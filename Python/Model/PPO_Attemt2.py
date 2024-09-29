import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from custom_robot_env import CustomRobotEnv,n_features,k_labels  # Import your custom environment


def main():
    # Create the custom Gym environment
    env = CustomRobotEnv(model_path='env_network.pth', input_size=n_features, output_size=k_labels)

    # Optionally, create a vectorized environment

    vec_env = make_vec_env(lambda: env, seed=None, n_envs=4)

    # Create and train the PPO agent
    model = PPO("MlpPolicy", vec_env, verbose=1,n_epochs=100)
    model.learn(total_timesteps=1000000)

    # Save the trained model
    model.save("ppoModels/ppoData3")



def continue_training():
    # Load the previously trained model
    # Load the previously trained model
    model = PPO.load("ppoModels/ppoData3_2Mil.zip")

    # Create the custom Gym environment
    env = CustomRobotEnv(model_path='env_network.pth', input_size=n_features, output_size=k_labels)

    # Optionally, create a vectorized environment
    vec_env = make_vec_env(lambda: env, seed=None, n_envs=4)

    # Set the environment for the model
    model.set_env(vec_env)

    # Continue training the model, Adjust total_timesteps as needed
    model.learn(total_timesteps=1000000)  

    # Save the updated model
    model.save("ppoModels/ppoData3_3Mil")
  
if __name__ == "__main__":
    #main()
    continue_training()
