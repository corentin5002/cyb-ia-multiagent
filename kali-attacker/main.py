from cyberattackenv import *

# Quick testing
if __name__ == "__main__":
    env = CyberAttackEnv()
    obs, _ = env.reset()
    done = False

    env.train(display=False)

    env.attack_for_real()

    env.close()

