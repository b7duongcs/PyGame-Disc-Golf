import torch
import random
import numpy as np
from collections import deque
from disc_golf_ai import DiscGolfAI
from model import Linear_QNet, QTrainer
from helper import plot

#⊂(◉‿◉)つ

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9 #<1
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 12)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        state = [
            #object positions
            game.disc.y,
            game.goal.x,
            game.goal.y,
            game.obstacle.x,
            game.obstacle.y,
            #parameters
            game.parameters.rotation,
            game.parameters.launch_speed,
            game.parameters.launch_va,
            game.parameters.launch_ha,
            game.parameters.nose,
            game.parameters.roll
        ]

        return np.array(state)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)
    
    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        self.epsilon = 500 - self.n_games
        action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            for i in range(len(action)):
                move = random.randint(0, 11)
                action[move] = 1
                #action[i] = random.uniform(0, 1)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            action[move] = 1
            #pred_array = prediction.detach().numpy()
            #for i, element in enumerate(pred_array):
            #    if pred_array[i] > 0:
            #        pred_array[i] = 1
            #    else:
            #        pred_array[i] = 0
            #print("prediction: ", pred_array) #change next two lines based on output to set action as new array
            ##round each element of prediction to 0 or 1
            #action = pred_array

        return action

def train():
    plot_dists = []
    plot_mean_dist = []
    total_dist = 0
    record = 10000
    time_adjust = 0
    agent = Agent()
    game = DiscGolfAI()

    while True:
        state_old = agent.get_state(game)
        action = agent.get_action(state_old)
        reward, game_over, min_distance, run_time = game.play_step(time_adjust, action)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old, action, reward, state_new, game_over)
        agent.remember(state_old, action, reward, state_new, game_over)

        if game_over:
            time_adjust += run_time

            game.reset()
            agent.n_games +=1
            agent.train_long_memory()

            if min_distance < record:
                record = min_distance
                agent.model.save()

            print('Game: ', agent.n_games, 'Distance: ', min_distance, 'Record: ', record)

            plot_dists.append(min_distance)
            total_dist += min_distance
            mean_dist = total_dist / agent.n_games
            plot_mean_dist.append(mean_dist)
            plot(plot_dists, plot_mean_dist)

if __name__ == '__main__':
    train()