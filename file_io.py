import pylab, os
from numpy import *
from numpy.linalg import *

def read_field(path):
    lines = file(path).readlines()
    lines = filter(lambda a : not a.startswith('n'),lines)

    x = array([line.strip().split()[0] for line in lines], float).T
    y = array([line.strip().split()[1] for line in lines], float).T
    vals = array([line.strip().split()[3] for line in lines], float).T
    nno = x.size 

    # sort by increasing x and then y values
    data = zeros((nno,),dtype=('f4, f4, f4'))
    for i in range(nno):
        data[i] = (x[i], y[i], vals[i])    
    data = sort(data, order=['f0','f1'])
    
    return nno, data['f0'], data['f1'], data['f2']

def read_J(path):

    path += "J.dat"
    J = loadtxt(path)

    return J[()]

def write_field(path, x, y, vals):
     
     f = open(path,'w')
     nno = x.size
     f.write('nnodes=%d\n' % nno)
     z = 0.0;
     for i in range(nno):
         f.write('%.10e\t' % x[i])
         f.write('%.10e\t' % y[i])
         f.write('%.10e\t' % z) 
         f.write('%.10e\n' % vals[i])
     
     f.close()
         
     return 

