import gym
from gym import spaces
import numpy as np
import random

class CyberAttackEnv(gym.Env):
    """
    Custom Environment for Q-learning training in cyber attack simulation.
    """
    def __init__(self):
        super(CyberAttackEnv, self).__init__()

        # Actions: 6 possible
        self.action_space = spaces.Discrete(6)

        # States: 7 binary features (open services + flags)
        self.observation_space = spaces.MultiBinary(7)

        # Initial state
        self.state = None
        self.steps = 0
        self.max_steps = 20

    def reset(self, seed=None, options=None):
        self.steps = 0

        # Randomly decide which services are open
        ftp = random.choice([0, 1])
        ssh = random.choice([0, 1])
        http = random.choice([0, 1])
        samba = random.choice([0, 1])
        postgres = random.choice([0, 1])

        # Flags for scan and exploitation
        scan_done = 0
        already_exploited = 0

        self.state = np.array([ftp, ssh, http, samba, postgres, scan_done, already_exploited], dtype=np.int8)

        return self.state, {}

    def step(self, action):
        self.steps += 1
        reward = -1  # small negative reward per action
        done = False

        ftp, ssh, http, samba, postgres, scan_done, already_exploited = self.state

        # Define action consequences
        if action == 0:  # scan_network
            scan_done = 1
            reward = random.choice([0, 5])

        elif action == 1:  # scan_ports
            if scan_done:
                reward = random.choice([5, 10])
            else:
                reward = -5

        elif action == 2:  # bruteforce_ftp
            if ftp:
                reward = random.choice([-10, 10])
            else:
                reward = -10

        elif action == 3:  # bruteforce_ssh
            if ssh:
                reward = random.choice([-10, 10])
            else:
                reward = -10

        elif action == 4:  # exploit_vsftpd
            if ftp:
                reward = random.choice([10, 10, -10])  # higher chance of success
                if reward > 0:
                    already_exploited = 10
            else:
                reward = -10

        elif action == 5:  # do_nothing
            reward = -2

        # Update state
        self.state = np.array([ftp, ssh, http, samba, postgres, scan_done, already_exploited], dtype=np.int8)

        # Episode done if exploited or steps exceeded
        if already_exploited or self.steps >= self.max_steps:
            done = True

        return self.state, reward, done, False, {}

    def play_q_table(self, Q_table):
        """
        Play the environment using the Q-table.
        """
        state, _ = self.reset()
        done = False

        while not done:
            action = np.argmax(Q_table[state])
            state, reward, done, _, _ = self.step(action)
            self.render()

            if done:
                print(f"Episode finished after {self.steps} steps with reward: {reward}")
                break

        return state, reward, done


    def render(self):
        print(f"Step {self.steps} - State: {self.state}")

    def close(self):
        pass

def random_action():
    """
    Randomly select an action from the action space.
    """
    return random.randint(0, 6)

def train():
    max_episodes = 1000

    env = CyberAttackEnv()
    state, _ = env.reset()

    # Q-learning parameters
    alpha = 0.1  # learning rate
    gamma = 0.9  # discount factor
    epsilon = 1  # exploration rate

    # Initialize Q-table
    state_space_size = (2, 2, 2, 2, 2, 2, 2)  # Binary state space
    action_space_size = 6 # Number of actions
    Q_table = np.zeros(state_space_size + (action_space_size,))

    print(Q_table.shape)
    for episode in range(max_episodes):
        done = False
        while not done:
            # Choose action (epsilon-greedy)
            if np.random.rand() < epsilon:
                action = random_action()
                print(action)
            else:
                action = np.argmax(Q_table[state])
                print(action)


            # Execute action (scan, bruteforce, exploit)
            next_state, reward, done, _, _ = env.step(action)
            state_key = tuple(state)
            Q_table[state, action] = Q_table[state_key, action] + alpha * (
                    reward + gamma * np.max(Q_table[next_state]) - Q_table[state_key, action]
            )

            state = next_state

    env.close()
    return Q_table

# Quick testing
if __name__ == "__main__":
    env = CyberAttackEnv()
    obs, _ = env.reset()
    done = False

    Q_table = train()

    env.render()
    env.play_q_table(Q_table)

    env.render()

    env.close()

