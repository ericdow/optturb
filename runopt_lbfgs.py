import pylab
from numpy import *
from numpy.linalg import *
from opt import opt
import file_io

path = "c004/"
restart = "restart.out"
niter = 50000 # max ifDual iterations
np = 6 # number of cores to run on

ctolpri = 2e-6
ctoladj = 1e-4

# read in initial turbulent viscosity
temp = path; temp+="nut_no.dat"
nno, x_no, y_no, nu0 = file_io.read_field(temp)

# create an instance of opt
o = opt(x_no, y_no, niter, restart, path, np, ctolpri, ctoladj)
tol = 1e-9
nopt = 500 # number of optimization iterations
x_opt, J_opt, res = o.lbfgs(nopt, nu0, tol)
nu_opt = exp(x_opt)

print J_opt

# write out mu_opt
temp = path; temp+="nut_opt"
file_io.write_field(temp, x_no, y_no, nu_opt)

