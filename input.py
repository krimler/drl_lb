import socket
import struct
import configparser  
import csv
import random

#alexa 1m https://gist.github.com/chilts/7229605

class population :
    population = 0
    start = 0
    end = 0
    weight = 0

    def __repr__(self):
        return '<%s object --> population[%d] (start[%d]:end[%d]) weight[%d]>' % (
               self.__class__.__name__,
               self.population,
               self.start,
               self.end,
               self.weight)

def ip2int(addr):                                                               
    return struct.unpack("!I", socket.inet_aton(addr))[0]                       


def int2ip(addr):                                                               
    return socket.inet_ntoa(struct.pack("!I", addr))   


def create_ip_range(min_mask, max_ip, ips):
   assert(min_mask >= 0 and min_mask < 31)
   min_mask = 2**min_mask
   ip_list = []
   with open(ips,  'w') as ip_file:
       count = 0 
       for i in range(max_ip):
           count += 1
           ip_file.write(int2ip(i + min_mask) + "\n" )
           ip_list.append(int2ip(i + min_mask))
   return ip_list

def generate_input(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    min_mask = int(config.get('input', 'min_mask'))
    max_ip = int(config.get('input', 'max_ip'))
    ips = config.get('input', 'ip_address')
    url_file = config.get('input', 'url_file')
    max_distributions = int(config.get('input', 'max_distributions'))
    iterations = int(config.get('input', 'iterations'))
    exp_input_file = config.get('input', 'experiement_input_file')
    ip_list = create_ip_range(min_mask, max_ip, ips) 
    urls = clean_alexa_file(url_file)

    distributions = []
    for i in range(max_distributions):
        p = population()
    
        p.population = i
        iindex = 'distribution'+ str(i)
        p.start = int(config.get(iindex, 'start'))
        p.end = int(config.get(iindex, 'end') )
        p.weight = int(config.get(iindex, 'weight'))
        
        distributions.append(p)
    return ip_list, urls, distributions, iterations, exp_input_file

    
def clean_alexa_file(top_file_csv):
    urls = []
    with open(top_file_csv, 'r') as top_csv:
        reader = csv.reader(top_csv, delimiter=',', quotechar='\n')
        for row in reader:
            urls.append(row[1])
    return urls
         

def get_ip_population_and_weight(ips, iterations):
    ip_population = []
    #request coming from each IP has same probability.
    for i in range(iterations):
        ip = random.randint(0, len(ips)-1)
        ip_population.append(ips[ip])
    return ip_population

class input_:
    def __init__(self, input_file):
        self.input_file = input_file

       
def generate_experiment_input_file(conf_file):      
    ips, urls, distributions, iterations, exp_input_file  = generate_input(conf_file)
    return_input_obj = input_(exp_input_file)
    ip_population = get_ip_population_and_weight(ips, iterations)

    population = []
    weights = []
    for d in distributions:
        population.append(d.population)
        weights.append(d.weight)
    with open(exp_input_file, 'w') as exp_file:
        for i in range(iterations):
            population_choice = random.choices(population, weights)
            population_choice = population_choice[0]
            iindex = random.randint(distributions[population_choice].start, distributions[population_choice].end)
            exp_file.write(ip_population[i] + ',' + urls[iindex] + '\n')
    return return_input_obj

if __name__ == '__main__':    
    generate_experiment_input_file(conf_file)    
