import matplotlib.pyplot as plt
from cyberattackenv import *

# Quick testing
if __name__ == "__main__":
    env = CyberAttackEnv()
    obs, _ = env.reset()
    done = False

    env.train(display=False)

    # plot the env.history
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))

    env.history_train.plot(x="episode", y="reward", title="Reward per episode", xlabel="Episode", ylabel="Reward", ax=axes[0], color="green")
    env.history_train.plot(x="episode", y="steps", title="Steps per episode", xlabel="Episode", ylabel="Steps", ax=axes[1], color="orange")
    env.history_train.plot(x="episode", y="epsilon", title="Epsilon per episode", xlabel="Episode", ylabel="Epsilon", ax=axes[2])

    plt.tight_layout()
    plt.show()

    env.save_q_table("q_table.npy")
    env.load_q_table("q_table.npy")

    env.play_q_table()

    env.close()

