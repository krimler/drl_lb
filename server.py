import os
import time
import redis
import random
import configparser
import util

class Servers_config:
    def __init__(self, conf_file):
        self.redis = False
        config = configparser.ConfigParser()
        config.read(conf_file)
        self.http_persistent_connection_size = int(config.get('output', 'http_persistent_connection_size'))
        self.max_iteration = int(config.get('output', 'max_iteration'))
        self.http_persistent_timeout = int(config.get('output', 'http_persistent_timeout'))
        self.persistent_hit_award = int(config.get('output', 'persistent_hit_award'))
        self.persistent_miss_award = int(config.get('output', 'persistent_miss_award'))
        policy = config.get('output', 'policy')
        self.policy_list = policy.split(',')
        ports = config.get('output', 'redis_servers_ports')
        self.port_list = list(map(int, ports.split(',')))
        self.total_servers = int(config.get('output', 'total_servers'))
        self.download_time = util.inter(config.get('output', 'download_time'))
        self.download_time_weight = util.floater(config.get('output', 'download_time_weight'))
        self.persistent_timeout = int(config.get('output', 'persistent_timeout'))
        self.report_file = config.get('output', 'report_file')
    def __repr__(self):
        return ('http_persistent_connection_size :' + str(self.http_persistent_connection_size) + '\n' + 
               'http_persistent_timeout :' + str(self.http_persistent_timeout) + '\n' + 
               'persistent_hit_award :' + str(self.persistent_hit_award) + '\n' +
               'persistent_miss_award :' + str(self.persistent_miss_award) + '\n' +
               'policy_list :' + str(self.policy_list) + '\n' + 
               'port_list :' + str(self.port_list) + '\n' +
               'total_servers :' + str(self.total_servers) + '\n' +
               'download_time :' + str(self.download_time) + '\n' +
               'download_time_weight :' + str(self.download_time_weight) + '\n' +
               'persistent_timeout :' + str(self.persistent_timeout) + '\n' +
               'report_file :' + self.report_file + '\n')
    def bringup_redis(self, handle_redis):
       self.redis = handle_redis
       if self.redis:
           os.system('sh redis.sh')
           time.sleep(5)
       print('bring redis up ------------>')
    def cleanup_redis(self):
        if self.redis:
            os.system('pkill redis')
        time.sleep(5)


server_config = Servers_config("config.ini")
class server :
    def __init__(self, port):
        self.r_live = redis.Redis(
        'localhost',
        port 
        )
        self.r_persistent = redis.Redis(
        'localhost',
        (port+1) 
        )

    def write_live_session(self, session):
        #self.r_live.set(session, '1', random.randint(1, 6)) #live session, it will live for 1 to 5 seconds.
        self.r_live.set(session, '1', util.distribution(server_config.download_time, server_config.download_time_weight))
    def write_persistent_session(self, session):
        self.r_persistent.set(session, '1', server_config.persistent_timeout) #persistent session, it will live for 300 seconds.
    def live_sessions(self):
        return self.r_live.dbsize()
    def persistent_sessions(self):
        return self.r_persistent.dbsize()
    def del_live_session(self, session):
        return self.r_live.delete(session)
    def del_persistent_session(self, session):
        return self.r_persistent.delete(session)
    def lookup_persistent_sessions(self, session):
        if not self.r_persistent.get(session):
            return False
        return True

def test_live_sessions():
    s = server(6379)
    s.write_live_session('foobar')
    s.write_live_session('barfoo')
    print(''+ str(s.live_sessions()))
    
    import time
    time.sleep(4)
    print(''+ str(s.live_sessions())) 

def test_persi_sessions():
    s = server(6379)
    s.write_persistent_session('foobar')
    print ('' + str(s.persistent_sessions()))
    print('' + str(s.lookup_persistent_sessions('foobar')))
     
    
    import time
    time.sleep(4)
    print(''+ str(s.persistent_sessions())) 
 
if __name__ == '__main__':
    print(server_config)
    
