import time
import gym
from gym import spaces
import numpy as np
import random
import os
from attack_functions import *

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

        self.had_waited = False

        # save for states
        self.ip_detected = None
        self.port_detected = None

        self.ip_selected = None
        self.ports_selected = []

        self.Q_table = None

    def reset(self, seed=None, options=None):
        self.steps = 0

        # Randomly decide which services are open
        self.ip_detected = 0
        self.ip_selected = None

        # self.ports_selected = random.sample([21, 22, 2121], random.randint(1, 3))
        self.ports_selected = []

        # Flags for scan and exploitation
        # self.state = np.array([self.ip_detected] + self.ports_detected_env_fmt(), dtype=np.int8)
        self.state = np.array([self.ip_detected, 0, 0, 0], dtype=np.int8)

        return self.state, {}

    def step(self, action, display=True):
        self.steps += 1
        reward = -1  # small negative reward per action
        done = False
        truncated = False

        ip_detected, ftp, ssh, vsftpd = self.state

        # Define action consequences
        if action == 0:  # wait
            self.had_waited = True
            reward = -2

        elif action == 1:  # scan for ip
            ip_detection_threshold = 0.5

            if self.had_waited :
                ip_detection_threshold += 0.2
                self.had_waited = False
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

                    if self.had_waited:
                        number_open_ports = np.min([1 + number_open_ports, 3])
                        self.had_waited = False

                    self.ports_selected = random.sample([21, 22, 2121], number_open_ports)
                    self.port_detected = True

        elif action in [3, 4, 5] and not self.ip_detected:
            reward = -50

        elif action == 3:  # bruteforce ftp
            done = True
            ftp_success_threshold = 0.1

            if 2121 in self.ports_selected:
                ftp_success_threshold += 0.8

            if random.random() < ftp_success_threshold :
                reward = 10
            else:
                reward = -10

        elif action == 4:  # bruteforce ssh
            done = True
            ssh_success_threshold = 0.1

            if 22 in self.ports_selected:
                ssh_success_threshold += 0.8

            if random.random() < ssh_success_threshold:
                reward = 10
            else:
                reward = -10

        elif action == 5:  # exploit vsftpd
            done = True
            vsftpd_success_threshold = 0.1

            if 21 in self.ports_selected:
                vsftpd_success_threshold += 0.8

            if random.random() < vsftpd_success_threshold:
                reward = 10
            else:
                reward = -10

        # Update state
        self.state = np.array([1 if self.ip_detected else 0] + self.ports_detected_env_fmt(), dtype=np.int8)

        if self.steps >= self.max_steps:
            if display:
                print("Max steps reached")
            truncated = True

        return self.state, reward, done, truncated, {}

    def ports_detected_env_fmt(self) -> list[int]:
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

        print("Playing with Q-table...")
        if Q_table is None:
            Q_table = self.Q_table

        while not done:
            action = np.argmax(Q_table[tuple(state)])
            state, reward, done, _, _ = self.step(action)
            self.render()

            if done:
                print(f"Episode finished after {self.steps} steps with reward: {reward}")
                break

        return state, reward, done

    def train(self, num_episode:int =1000,display:bool =True):

        alpha = 0.1
        gamma = 0.9
        epsilon = 1
        epsilon_decay     = 0.995

        self.Q_table = np.zeros((2, 2, 2, 2, 6))

        rewards_sum_history = []

        for episode in range(num_episode):

            state, _ = self.reset()
            done = False
            truncated = False
            reward_sum = 0
            if display:
                print('\n')
                self.render(None, reward_sum)

            while not (done or truncated):
                if random.uniform(0, 1) < epsilon:
                    action = random.choice(range(self.action_space.n))

                else:
                    action = np.argmax(self.Q_table[tuple(state)])

                next_state, reward, done, truncated, _ = self.step(action, display=False)

                # Update Q-table
                self.Q_table[tuple(state)][action] += alpha * (reward + gamma * np.max(self.Q_table[tuple(next_state)]) - self.Q_table[tuple(state)][action])
                state = next_state
                reward_sum += reward

                if display:
                    self.render(action, reward_sum)

                if done or truncated:
                    if display:
                        print(f"Episode {episode} finished after {self.steps} steps with reward: {reward}")
                    break

            # Decay epsilon
            if epsilon > 0.05:
                epsilon *= epsilon_decay

    def render(self, action=None, reward=None):
        render_output = f"Step {self.steps} - State: {self.state}"
        render_output += f" - Action: {action}" if action is not None else ""
        render_output += f" - Reward: {reward}" if reward is not None else ""

        print(render_output)

    def close(self):
        pass

    def save_q_table(self, Q_table_path: str):
        """
        Save the Q-table to a .npy file.
        """

        if not Q_table_path.endswith(".npy"):
            Q_table_path += ".npy"

        np.save(Q_table_path, self.Q_table)
        print(f"Q-table successfully saved to {Q_table_path}")

    def load_q_table(self, Q_table_path: str):
        """
        Load a Q-table from a .npy file.
        """

        if not Q_table_path.endswith(".npy"):
            Q_table_path += ".npy"

        if not os.path.exists(Q_table_path):
            raise FileNotFoundError(f"The file {Q_table_path} does not exist!")

        try:
            loaded_table = np.load(Q_table_path)

            if loaded_table.shape != self.Q_table.shape:
                print(
                    f"Warning: Loaded Q-table shape {loaded_table.shape} does not match expected {self.Q_table.shape}")

            self.Q_table = loaded_table
            print(f"Q-table successfully loaded from {Q_table_path}")

        except Exception as e:
            print(f"Failed to load Q-table: {e}")

    def attack_for_real(self):
        """
        Execute the attack using the Q-table.
        """
        self.reset()
        done = False
        print("[*] Launching real-world attack using Q-table...")

        while not done:
            # print(f"[*] Current state: {self.state}")
            print(f"[*] q_table type: {type(self.Q_table)}")
            state_tuple = tuple(int(x) for x in self.state)
            action = np.argmax(self.Q_table[state_tuple])

            if action == 0:  # Wait
                print("[*] Waiting... (no action)")
                time.sleep(3)

            elif action == 1:  # Scan for IPs
                print("[*] Scanning for active IPs...")
                active_ips = get_active_ips()

                if active_ips:
                    self.ip_selected = active_ips[0]
                    self.ip_detected = True
                    print(f"[+] Target IP detected: {self.ip_selected}")

                else:
                    self.ip_detected = False
                    self.ip_selected = None
                    print("[-] No target IP found.")

            elif action == 2:  # Scan for ports
                if not self.ip_detected:
                    print("[-] No IP detected yet. Skipping port scan.")
                else:
                    print(f"[*] Scanning open ports on {self.ip_selected}...")
                    open_ports = get_active_ports(self.ip_selected)
                    if open_ports:
                        self.ports_selected = [int(p) for p in open_ports]
                        self.port_detected = True
                        print(f"[+] Open ports found: {self.ports_selected}")
                    else:
                        self.ports_selected = []
                        self.port_detected = False
                        print("[-] No open ports detected.")

            elif action == 3:  # Bruteforce FTP
                if not self.ip_detected:
                    print("[-] No IP detected. Cannot bruteforce FTP.")
                else:
                    print(f"[*] (Would bruteforce FTP on {self.ip_selected})")
                    attack_ftp(self.ip_selected)

            elif action == 4:  # Bruteforce SSH
                if not self.ip_detected:
                    print("[-] No IP detected. Cannot bruteforce SSH.")
                else:
                    print(f"[*] (Would bruteforce SSH on {self.ip_selected})")
                    attack_ssh(self.ip_selected)

            elif action == 5:  # Exploit vsftpd
                if not self.ip_detected:
                    print("[-] No IP detected. Cannot exploit vsftpd.")
                else:
                    print(f"[*] (Would exploit vsftpd on {self.ip_selected})")
                    attack_vsftpd(self.ip_selected)

            # -------- UPDATE STATE MANUALLY BASED ON REALITY --------
            # ports_selected = [21, 22, 2121]
            ftp_detected = 1 if 2121 in self.ports_selected else 0
            ssh_detected = 1 if 22 in self.ports_selected else 0
            vsftpd_detected = 1 if 21 in self.ports_selected else 0

            self.state = np.array([
                1 if self.ip_detected else 0,
                ftp_detected,
                ssh_detected,
                vsftpd_detected
            ], dtype=np.int8)

            # step forward
            self.steps += 1
            self.render(action=action)

            if action in [3, 4, 5]:  # Bruteforce/Exploit actions => End attack
                done = True

            if self.steps >= self.max_steps:
                print("[*] Max steps reached.")
                done = True

        print(f"[*] Attack finished after {self.steps} steps.")
        return self.state