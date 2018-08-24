import random
import time
import our_gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

EPISODES = 1000


class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=20000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.009
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        #https://keras.io/activations/ 
        model.add(Dense(1024, activation='hard_sigmoid'))
        model.add(Dense(1024, activation='hard_sigmoid'))
        model.add(Dense(1024, activation='hard_sigmoid')) 
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            ret = random.randrange(self.action_size)
            return ret
        act_values = self.model.predict(state)
        ret = np.argmax(act_values[0])
        return ret

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state in minibatch:
            target = reward
            target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state, batch_size, 0, None)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        time.sleep(0)


    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
#https://github.com/openai/gym/blob/master/gym/envs/robotics/robot_env.py
#https://github.com/keon/deep-q-learning/blob/master/dqn.py
#https://github.com/openai/gym/blob/master/gym/envs/robotics/robot_env.py
class DRL:
    def __init__(self, total_servers ):
        self.env = our_gym.LB(total_servers)
        self.state_size = self.env.state_shape()
        self.action_size  = self.env.action_shape()
        self.last_state = 0.0
        self.last_state = 0
    
        self.agent = DQNAgent(self.state_size, self.action_size)
        self.batch_size = 100
        self.lb_state = self.env.reset()
        self.action = 0
        self.next_state = 0.0
        self.reward = 0
        self.lb_hash = 0
    def do(self, s, d, s0, s1, s2 ): 
        lb_state  = self.env.set_state(s, d, s0, s1, s2)
        self.lb_hash = self.lb_state.do_hash()
        self.action = self.agent.act(self.lb_hash)

        return self.action
    def update(self, persi_hit, s0, s1, s2):
        self.reward = 0
        if persi_hit:
            self.reward = 20
        else :
            self.reward = -10

        self.next_state = self.lb_state.re_init(s0, s1, s2)
        if self.next_state.std_dev < 100:
            self.reward += 3
        if self.next_state.std_dev < 50:
            self.reward +=  5
        elif self.next_state.std_dev < 10:
            self.reward += 12
        else:
            self.reward -= 20
 
        self.agent.remember(self.lb_state.do_hash(), self.action, self.reward, self.next_state.do_hash())

    def replay(self):
        if len(self.agent.memory) > self.batch_size:
            self.agent.replay(self.batch_size) 
        else :
            pass
if __name__ == "__main__":
    drl = DRL(3)
    
