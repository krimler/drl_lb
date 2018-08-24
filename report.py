import os
import util

class Report:
    def __init__(self, file_name, mode):
        self.reported_policy = ''
        self.total_sessions = 0
        self.session_distribution = []
        self.persistent_hits = 0
        self.report_file = open(file_name, mode)

    def move(self, header):
        self.report_file.write(header + '\n')

    def done(self):
        self.report_file.close() 

    def process(self, policy, session_distribution, total_sessions, persistent_hits):
        log = policy + ' ,\t' + util.lister(session_distribution) + str(total_sessions) + ' ,\t' + str(persistent_hits) + '\n'
        #print(log)
        self.report_file.write(log)
        self.report_file.flush()
        os.fsync(self.report_file)

if __name__ == '__main__':
    r = Report('foobar', 'started')
    r.move('do more')
    for i in range(2):
        r.process('policy', [1, 2, 3], 5, 1000)
 
    r.done()
        
