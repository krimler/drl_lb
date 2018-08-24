import server
import policy
import input

class Mechanism:
    def __init__(self):
        self.server_config = server.server_config
        self.servers = self.get_servers()
        self.total_servers = len(self.servers)
        self.policy_obj = policy.Policy(self.total_servers)
        self.current_connection_count_list = []
        for each in self.servers:
            self.current_connection_count_list.append(0)
       
        self.last_server = 0
        self.curr_conn_list = []
        self.policy = policy.Policy(self.total_servers)
        self.persi_hit = 0
    def get_servers(self):
        servers = []
        for each_port in self.server_config.port_list:
            server_ = server.server(each_port)
            servers.append(server_)
        return servers;
    def __get_connection_list__(self):
        total_conn_list = []
        for each in self.servers:
            total_conn_list.append(each.live_sessions())
        return total_conn_list

    def __repr__(self):
        return ('conn list: ' + str(self.curr_conn_list) + '; persistence: ' + str(self.persi_hit)  + '; server id: ' + str(self.last_server) ) 

    def do(self, policy_string, sources, destinations):
        iindex = 0
        self.persi_hit = 0
        persistent = 0
        for src, dest in zip(sources, destinations):
            #print(src + '____' + dest + '---------]' + str(iindex))

            iindex += 1
            self.curr_conn_list = self.__get_connection_list__()
            self.last_server = policy.eval(self.policy_obj, policy_string, self.total_servers, self.last_server, src, dest, self.curr_conn_list, persistent) 
            persistent = self.servers[self.last_server].lookup_persistent_sessions(src+dest)
            if persistent:
                self.persi_hit += 1

        
            self.servers[self.last_server].write_persistent_session(src+dest)
            self.servers[self.last_server].write_live_session(src+dest)
            if policy_string == 'deep_reinforcement':
                self.policy_obj.drl_update(persistent, self.__get_connection_list__())
        # replay before finishing up this trend.
        self.policy_obj.drl_replay()
        return (policy_string, self.curr_conn_list, self.persi_hit) 
            

if __name__ == '__main__':
        pass    

         
