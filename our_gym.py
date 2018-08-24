import numpy as np

class LB_state:
    def __init__(self, s, d, s0, s1, s2):
        self.src = s
        self.dest = d
        self.server0_load = s0
        self.server1_load = s1
        self.server2_load = s2
        #compute standard_deviation.
       
        arr = np.array([self.server0_load, self.server1_load, self.server2_load])
        self.std_dev = np.std(arr)
    def re_init(self, s0, s1, s2):
        lb = LB_state('', '', 0, 0, 0)
        lb.src = self.src
        lb.dest = self.dest
        lb.server0_load = s0
        lb.server1_load = s1
        lb.server2_load = s2
        #compute standard_deviation.
       
        arr = np.array([lb.server0_load, lb.server1_load, lb.server2_load])
        lb.std_dev = np.std(arr)
        return lb
    def reset(self, s, d, s0, s1, s2):
        self.src = s
        self.dest = d
        self.server0_load = s0
        self.server1_load = s1
        self.server2_load = s2
        #compute standard_deviation.

        arr = np.array([self.server0_load, self.server1_load, self.server2_load])
        self.std_dev = np.std(arr)
    def __do_hash__(self, string):
          #https://stackoverflow.com/questions/2909106/whats-a-correct-and-good-way-to-implement-hash
          hash = 0
          for c in string:
              hash = 31 * hash  +  ord(c)
          return hash
    def do_hash(self):
        my_hash = np.array([[self.__do_hash__(self.src)%2000],  [self.__do_hash__(self.dest)%1000000], [str(int(self.std_dev))]])
        return my_hash

def gym_max():
        # 2000 unique IPs
        # 1 million URLs
        return 1
class LB:
    def __init__(self, servers_available):
        self.action_sz = servers_available
        self.state_sz =  gym_max()
        self.state = LB_state('', '', 0, 0, 0)
    def reset(self):
        self.state = LB_state('', '', 0, 0, 0)
        return self.state
    def set_state(self, s, d, s0, s1, s2):
        self.state.reset(s, d, s0, s1, s2)
        return self.state
    def state_shape(self):
        return self.state_sz
    def action_shape(self):
        return self.action_sz
