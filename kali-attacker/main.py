import gym
from gym import spaces
import numpy as np
import random

# FILTER THIS IP ITS THE OWNER (myself)
# 192.168.10.1

class CyberAttackEnv(gym.Env):
    """
    Custom Environment for Q-learning training in cyber attack simulation.
    """
    def __init__(self):
        super(CyberAttackEnv, self).__init__()

        # Gym environment variables for Q_learning
        # Actions :
        # - Wait
        # - Scan network (search for IPs)
        # - Scan ports
        # - Bruteforce FTP
        # - Bruteforce SSH
        # - Exploit vsftpd
        self.action_space = spaces.Discrete(6)

        # states :
        # - IP found
        # - FTP port open
        # - SSH port open
        # - vsftpd port open
        self.observation_space = spaces.MultiBinary(4)

        self.state = None
        self.steps = 0
        self.max_steps = 20

        # save for states
        self.ip_detected = None
        self.port_detected = None

        self.ip_selected = None
        self.ports_selected = None

        self.Q_table = None

    def reset(self, seed=None, options=None):
        self.steps = 0

        # Randomly decide which services are open
        ip_detected = 0
        ftp = random.choice([0, 1])
        ssh = random.choice([0, 1])
        vsftpd = random.choice([0, 1])

        # Flags for scan and exploitation
        self.state = np.array([ip_detected, ftp, ssh, vsftpd], dtype=np.int8)

        return self.state, {}

    def step(self, action):
        self.steps += 1
        reward = -1  # small negative reward per action
        done = False
        truncated = False

        ip_detected, ftp, ssh, vsftpd = self.state

        # Define action consequences
        if action == 0:  # wait
            reward = -2

        elif action == 1:  # scan for ip
            ip_detection_threshold = 0.2
            # generated random float between 0 and 1
            ip_detected = random.random() < ip_detection_threshold

            if ip_detected:
                self.ip_selected = '192.168.10.1'
                self.ip_detected = True

        elif action == 2: # scan for port
            if not ip_detected:
                pass

            else:
                # Randomly select a port
                port_detection_threshold = 0.8
                port_detected = random.random() < port_detection_threshold

                if port_detected:
                    number_open_ports = random.randint(1, 3)

                    self.ports_selected = random.sample([21, 22, 2121], number_open_ports)
                    self.port_detected = True


        elif action == 3:  # bruteforce ftp
            done = True
            ftp_success_threshold = 0.1

            if 2121 in self.ports_selected:
                ftp_success_threshold += 0.5

            if random.random() < ftp_success_threshold :
                reward = 10
            else:
                reward = -10

        elif action == 4:  # bruteforce ssh
            done = True
            ssh_success_threshold = 0.1

            if 22 in self.ports_selected:
                ssh_success_threshold += 0.5

            if random.random() < ssh_success_threshold:
                reward = 10
            else:
                reward = -10

        elif action == 5:  # exploit vsftpd
            done = True
            vsftpd_success_threshold = 0.1

            if 21 in self.ports_selected:
                vsftpd_success_threshold += 0.5

            if random.random() < vsftpd_success_threshold:
                reward = 10
            else:
                reward = -10

        # Update state
        self.state = np.array([self.ip_detected] + self.ports_detected(), dtype=np.int8)

        if self.steps >= self.max_steps:
            truncated = True

        return self.state, reward, done, truncated, {}

    def ports_detected(self) -> list[int]:
        """
        Return the state of the ports detected.
        ports symbols : [ftp, ssh, vsftpd]
        """
        if self.port_detected:
            return [1 if port in self.ports_selected else 0 for port in [2121, 22, 21]]
        else:
            return [0, 0, 0]

    def play_q_table(self, Q_table=None):
        """
        Play the environment using the Q-table.
        """
        state, _ = self.reset()
        done = False


        if Q_table is None:
            Q_table = self.Q_table

        while not done:
            action = np.argmax(Q_table[state])
            state, reward, done, _, _ = self.step(action)
            self.render()

            if done:
                print(f"Episode finished after {self.steps} steps with reward: {reward}")
                break

        return state, reward, done

    def train(self, num_episode=1000):

        alpha = 0.1
        gamma = 0.9
        epsilon = 1
        epsilon_decay     = 0.995

        self.Q_table = np.zeros((2, 2, 2, 2, 6))

        for episode in range(num_episode):

            state, _ = self.reset()
            done = False

            while not done:
                if random.uniform(0, 1) < epsilon:
                    action = self.action_space.sample()
                else:
                    action = np.argmax(self.Q_table[state])
                next_state, reward, done, truncated, _ = self.step(action)

                # Update Q-table
                self.Q_table[tuple(state)][action] += alpha * (reward + gamma * np.max(self.Q_table[tuple(next_state)]) - self.Q_table[tuple(state)][action])
                state = next_state
                self.render()
                if done:
                    print(f"Episode {episode} finished after {self.steps} steps with reward: {reward}")
                    break

            # Decay epsilon
            if epsilon > 0.05:
                epsilon *= epsilon_decay


    def render(self):
        print(f"Step {self.steps} - State: {self.state}")

    def close(self):
        pass



def random_action():
    """
    Randomly select an action from the action space.
    """
    return random.randint(0, 6)


# Quick testing
if __name__ == "__main__":
    env = CyberAttackEnv()
    obs, _ = env.reset()
    done = False

    env.train()

    env.render()
    env.play_q_table()

    env.render()

    env.close()

