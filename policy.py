import dqn
def eval(policy, policy_string, total_servers, last_server, source, destination, current_connection_count_list, last_source_persistent_success):
        policy.policy_name = policy_string
        if policy_string == 'round_robin':
            return policy.__round_robin_based__(total_servers, last_server)
        if policy_string == 'least_connection':
            return policy.__least_connection_based__(total_servers, current_connection_count_list)
        if policy_string == 'source_hash':
            return policy.__source_hash_based__(total_servers, source)
        if policy_string == 'destination_hash':
            return policy.__destination_hash_based__(total_servers, destination)
        if policy_string == 'reinforcement':
            return policy.__reinforcement_based__(total_servers, source, destination, current_connection_count_list, last_source_persistent_success)
        if policy_string == 'deep_reinforcement' :
            return policy.__deep_reinforcement_based__(total_servers, source, destination, current_connection_count_list, last_source_persistent_success)
        return 'error'


class Policy:
    def __init__(self, total_servers):
        self.drl = dqn.DRL(total_servers)
        self.policy_name = ''
    def __round_robin_based__(self, total_servers, last_server):
        next = last_server + 1
        next = next % total_servers
        return next
    def __least_connection_based__(self, total_servers, current_connection_count_list):
        low_i = 0
        low_val = 0
        for i, val in enumerate(current_connection_count_list):
            if i == 0:
                low_val = val
            else:
                if val < low_val:
                    low_i = i
                    low_val = val
        return low_i
    def __do_hash__(self, string):
        #https://stackoverflow.com/questions/2909106/whats-a-correct-and-good-way-to-implement-hash
        hash = 0
        for c in string:
            hash = 101 * hash  +  ord(c)
        return hash
    def __source_hash_based__(self, total_servers, source):
        #in-built hash function
        return (self.__do_hash__(source) % total_servers)

    def __destination_hash_based__(self, total_servers, destination):
        return (self.__do_hash__(destination) % total_servers)

    def __source_and_destination_hash__(self, total_servers, source, destination):
        return (self.__do_hash__(source+destination) % total_servers)

    def __reinforcement_based__(self, total_servers, source, destination, current_connection_count_list, last_source_persistent_success):
        return 0

    def __deep_reinforcement_based__(self, total_servers, source, destination, current_connection_count_list, last_source_persistent_success):
        #computer standard deviation for live connections on servers. It is used as state space for DQN.
        return self.drl.do(source, destination, current_connection_count_list[0],
                                    current_connection_count_list[1],
                                    current_connection_count_list[2]) 
        
    def drl_update(self, persi_hit, current_connection_count_list) :
        if self.policy_name == 'deep_reinforcement' :
            self.drl.update(persi_hit, current_connection_count_list[0], current_connection_count_list[1], current_connection_count_list[2])
   
    def drl_replay(self):
        if self.policy_name == 'deep_reinforcement' :
            self.drl.replay() 


if __name__ == '__main__':
    policy = Policy(3)
    
    i = policy.__round_robin_based__(3, 0)
    j = policy.__round_robin_based__(3, 2)
    k = policy.__round_robin_based__(3, 3)
    m = policy.__round_robin_based__(3, 4)
    print(i)
    print(j)
    print(k)
    print(m)
   

  
    i = policy.__least_connection_based__(3, [1, 1, 1])
    print(i)
    i = policy.__least_connection_based__(3, [2, 3, 1])
    print(i)
    i = policy.__least_connection_based__(3, [2000, 1, 30000])
    print(i)
    i = policy.__least_connection_based__(3, [20000, 10000000, 10000])
    print(i)
 
    
    i = policy.__source_hash_based__(3, '1.2.3.4')
    print(i)
    i = policy.__source_hash_based__(3, '127.34.54.12') 
    print(i)
    i = policy.__source_hash_based__(3, '1.2.3.6')
    print(i)
