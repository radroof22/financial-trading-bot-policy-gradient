import torch

from Environment import Environment
from regular_policy import Agent, select_action, format_action

env = Environment()

# CONSTANTS
MODEL_PATH = "models/regular/model_BUFFET_WATERS.pt"
N_TESTS = 125

agent = Agent().cuda()
agent.load_state_dict(torch.load(MODEL_PATH))   

f = open("models/tests/BUFFET_WATERS_final.csv", "w")

if __name__ == "__main__":
    history = []
    
    for episode in range(N_TESTS):
        
        state = env.reset() # Reset environment and record the starting state
        episode_actions = {
            "hold": 0,
            "buy": 0,
            "sell": 0
        }
        
        done = False
        while not done:
            
            # Step through environment using chosen action
            actions = select_action(state.values.reshape(env.observation_space))
            action_dict = format_action(actions, monitor=False)

            state, reward, done = env.step(action_dict)

            agent.reward_episode.append(reward)

        env_change = env.net_change()
        cash_change = (reward - 100000 ) / 100000
        history.append((reward, env_change, cash_change, env.stock_list[env.stock_i]))
        
        print("Episode {} \t {}".format(episode+1, reward))

    # Stock Statistics and Preformance
    f.write("Last Balance,Environment Change,Agent Portfolio Change, Stock Name\n")
    for e in history:
        f.write(f"{e[0]},{e[1]},{e[2]}, {e[3]}\n")
        

