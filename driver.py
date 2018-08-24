import os
import csv
import sys
import pandas
import input
import server
import mechanism
import report
import dispositions
class Driver:
    def __init__(self, generate_input, policy_string, mode, conf_file):
       self.policy_string = policy_string
       self.generate_input = generate_input
       self.report_ = report.Report(server.server_config.report_file, mode)
       self.mode = mode
       if generate_input:
           print('generating input') 
           self.input_ = input.generate_experiment_input_file(conf_file)
           print('done with input generation') 
       else:
           self.input_ = "exp_input.txt"

    def set_header(self, servers):
        server_list = ''
        for i, val in enumerate(servers):
            server_list += 'server_' + str(i) + ', '
        self.report_.move('policy' + ', ' + server_list + 'total_session' + ', ' + 'persistent_hits')       

    def measure(self): 
       mechanism_ = mechanism.Mechanism()
       servers = mechanism_.get_servers()
       if self.mode == 'w':
           self.set_header(servers)

       iindex = -1
       sources = []
       dests = []
       
       ip_file = ''
       if self.generate_input:
           ip_file = self.input_.input_file
       else:
           ip_file = self.input_
       total_sessions = 0
       print('ip_file is ' + ip_file)
       with open(ip_file, "r") as ins:
           source = 0
           dest = 0
           for line in ins:
               iindex += 1
               ip, url = line.split(',')
               url = url.strip('\n')
               sources.append(ip)
               dests.append(url)
               if(iindex == server.server_config.max_iteration):
                   reported_policy, session_distribution, persistent_hits = mechanism_.do(self.policy_string, sources, dests)
                   self.report_.process(reported_policy, session_distribution, total_sessions, persistent_hits)
                   iindex = 0
                   source = []
                   dests = []
                   total_sessions += 1
               else:
                   total_sessions += 1
           reported_policy, session_distribution, persistent_hits = mechanism_.do(self.policy_string, sources, dests)
           self.report_.process(reported_policy, session_distribution, total_sessions, persistent_hits) 
           self.report_.done() 

if __name__ == '__main__':

    for config_file in dispositions.configs:
        server.server_config = server.Servers_config(config_file)
        policies = server.server_config.policy_list
        done = False
        policy = ''
        for i, each in enumerate(policies):
            policy  = each.strip() 
            if not done:
                mode = 'w'
                done = True
            else:
                mode = 'a' 
            print('Drive config : ' + config_file + '; policy: ' + policy)
            d = Driver(False, policy, mode, config_file)
            server.server_config.bringup_redis(True)
            d.measure()
            server.server_config.cleanup_redis()
        pass

