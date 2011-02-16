import pylab
import nlopt
from numpy import *
from numpy.linalg import *
import run_ifdual
import file_io
import shutil

# always start from the same velocity profile
# TO DO:
#  read in baseline viscosity profile to keep bounds consistent
#  baseline viscosity stored in nut_noRANS.dat - this is the
#  RANS viscosity profile.

class opt:
    # initialize class with:
    # - x_no/y_no (coordinate data)
    # - niter (max iterations to run in ifDual)
    # - restart (restart that will be used always)
    # - path (path where files are stored)
    # - np (number of cores to run on) 
    def __init__(self, x_no, y_no, niter, restart, path, np, ctolpri, ctoladj):
        self.x_no    = x_no
        self.y_no    = y_no
        self.niter   = niter
        self.restart = restart
        self.path    = path
        self.np      = np 
        self.ctolpri = ctolpri
        self.ctoladj = ctoladj
        self.count   = 0 # iteration number

    def J(self, x, grad):
        # x is ln(nu)
        # write out nut_no.dat so that it can be read in 
        nu = exp(x)
        temp = self.path; temp += "nut_no.dat"
        file_io.write_field(temp, self.x_no, self.y_no, nu)
        # solve flow at this nu
        f = open('runopt.out','a')
        f.write(''.join(['Running primal from ',self.restart,'...\n']))
        f.close()
        run_ifdual.runpri(self.path, self.restart, self.niter, self.np, self.ctolpri)
        f = open('runopt.out','a')
        f.write('Done running primal\n')
        f.close()
        src = ''.join([self.path,'ifDual.out'])
        dst = ''.join([self.path,'ifDual_Pri.step',str(self.count),'.out'])
        shutil.copy(src,dst)
        # read in objective function value
        J = file_io.read_J(self.path)
        # calculate gradient - call adjoint
        if grad.size > 0:
            f = open('runopt.out','a')
            f.write(''.join(['Running adjoint from ',self.restart,'...\n']))
            f.close()
            run_ifdual.runadj(self.path, self.restart, self.niter, self.np, self.ctoladj)
            f = open('runopt.out','a')
            f.write('Done running adjoint\n')
            f.close()
            # read in the gradient
            temp = self.path; temp += "grad.dat"
            nno, self.x_no, self.y_no, grad[:] = file_io.read_field(temp)
        # move files around
        f = open('runopt.out','a')
        f.write('Writing files for step %d\n' % self.count )
        f.close()
        src = ''.join([self.path,'J.dat'])
        dst = ''.join([self.path,'J.step',str(self.count),'.dat'])
        shutil.copy(src,dst)
        src = ''.join([self.path,'nut_no.dat'])
        dst = ''.join([self.path,'nut_no.step',str(self.count),'.dat'])
        shutil.copy(src,dst)
        src = ''.join([self.path,'grad.dat'])
        dst = ''.join([self.path,'grad.step',str(self.count),'.dat'])
        shutil.copy(src,dst)
        src = ''.join([self.path,'restart.out'])
        dst = ''.join([self.path,'restart.step',str(self.count),'.out'])
        shutil.copy(src,dst)
        src = ''.join([self.path,'ifDual.out'])
        dst = ''.join([self.path,'ifDual_Adj.step',str(self.count),'.out'])
        shutil.copy(src,dst)
        f = open('runopt.out','a')
        f.write('Iter: %d\t' % self.count)
        f.write('J = %.10e\n' % J)
        f.close()
        self.count+=1

        return J

    def lbfgs(self, maxeval, nu0, tol):
        n = nu0.size
        o = nlopt.opt(nlopt.LD_LBFGS, n)
        # tolerance on objective function value
        o.set_ftol_rel(tol)
        o.set_maxeval(maxeval)
        o.set_min_objective(self.J)
        # read in the baseline RANS viscosity for bounds
        temp = self.path; temp += "nut_noRANS.dat"
        j1, j2, j3, nu_base = file_io.read_field(temp)
        # constrain mu to be greater than 0.75 * baseline
        # o.set_lower_bounds(log(0.10*nu_base))
        # constrain mu to be less than 1.5 * baseline
        # o.set_upper_bounds(log(10.0*nu_base))
        # call the optimizer - pass in initial viscosity
        f = o.optimize(log(nu0))
        minf = o.last_optimum_value()
        res = o.last_optimize_result()

        return f, minf, res

