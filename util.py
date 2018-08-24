import numpy
def lister(ll):
        string = ''
        for each in ll:
            string += str(each) + ' ,\t'
        return string
def inter(string):
    ll = string.split(',')
    int_list = []
    for each in ll:
        int_list.append(int(each))
    return int_list

def floater(string):
    ll = inter(string)
    ff = []
    for each in ll:
        each = float(each)/100
        ff.append(each)
    return ff

def distribution(values, probs):
    #res = numpy.random.choice(d_list, 1, p = f_list)
    res = numpy.random.choice(values, 1, p=probs)
    res = res[0]
    return res    
'''
d = '1,  2,  3,  5,  10, 15, 20, 25, 30, 60, 300'
d_list = inter(d)
print(d_list)
download_time_weight = '30, 25, 20, 12, 6,  2,  1,  1,  1,  1,  1'
f_list = floater(download_time_weight)
print(f_list)
import numpy
res = numpy.random.choice(d_list, 1, p = f_list) 
print(res)
'''
        
      
