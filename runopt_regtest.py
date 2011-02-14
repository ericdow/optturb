import pylab
from numpy import *
from numpy.linalg import *
from opt import opt
import file_io

path = "reg_test/"
restart = "restart.out"
niter = 1 # max ifDual iterations

# read in initial turbulent viscosity
temp = path; temp+="nut_no.dat"
nno, x_no, y_no, nu0 = file_io.read_field(temp)

# create an instance of opt
o = opt(x_no, y_no, niter, restart, path)
tol = 1e-9
nopt = 200 # number of optimization iterations
x_opt, J_opt, res = o.lbfgs(nopt, nu0, tol)
nu_opt = exp(x_opt)

print J_opt

# write out mu_opt
temp = path; temp+="nu_opt"
file_io.write_field(temp, x_no, y_no, nu_opt)

