import os, string, fileinput

in_file = 'ifDual_channel.in'
out_file = 'ifDual.out'
call = ' /home/ericdow/code/ttadj/ifDualAdj '

def runadj(path, restart, nsteps, np, ctol):

    prev = os.getcwd()
    os.chdir(path)

    # change the restart file that will be used
    lines = open(in_file,'r').readlines()
    i = 0
    for line in lines:
        if line[0:7] == 'RESTART':
            del lines[i]
        i+=1

    # change number of steps
    i = 0
    for line in lines:
        if line[0:6] == 'NSTEPS':
            del lines[i]
        i = i+1

    # change timestep
    i = 0
    for line in lines:
        if line[0:2] == 'DT':
            del lines[i]
        i = i+1

    # change converge tol
    i = 0
    for line in lines:
        if line[0:12] == 'CONVERGE_TOL':
            del lines[i]
        i = i+1

    rep = 'NSTEPS = '
    rep += str(nsteps)
    rep += '\n'
    lines.append(rep)
    rep = 'DT = 0.0075\n'
    lines.append(rep)
    rep = 'RESTART = '
    rep += restart
    lines.append(rep)
    rep = 'CONVERGE_TOL = '
    rep += str(ctol)
    lines.append(rep)
    open(in_file,'w').writelines(lines)

    # call ifDual...
    cmd = ''.join(['mpirun -np ',str(np),call,'0 > ',out_file,' &'])
    print ''.join(['Running Adjoint from ',restart,'...'])
    os.system(cmd)
    print 'Done running Adjoint'
    os.chdir(prev)

    return

def runpri(path, restart, nsteps, np, ctol):

    prev = os.getcwd()
    os.chdir(path)

    # change the restart file that will be used
    lines = open(in_file,'r').readlines()
    i = 0
    for line in lines:
        if line[0:7] == 'RESTART':
            del lines[i]
        i+=1

    # change number of steps
    i = 0
    for line in lines:
        if line[0:6] == 'NSTEPS':
            del lines[i]
        i = i+1

    # change timestep
    i = 0
    for line in lines:
        if line[0:2] == 'DT':
            del lines[i]
        i = i+1

    # change converge tol
    i = 0
    for line in lines:
        if line[0:12] == 'CONVERGE_TOL':
            del lines[i]
        i = i+1

    rep = 'NSTEPS = '
    rep += str(nsteps)
    rep += '\n'
    lines.append(rep)
    rep = 'DT = 0.01\n'
    lines.append(rep)
    rep = 'RESTART = '
    rep += restart
    lines.append(rep)
    rep = 'CONVERGE_TOL = '
    rep += str(ctol)
    lines.append(rep)
    open(in_file,'w').writelines(lines)

    # call ifDual...
    cmd = ''.join(['mpirun -np ',str(np),call,'2 > ',out_file,' &'])
    print ''.join(['Running Primal from ',restart,'...'])
    os.system(cmd)
    print 'Done running Primal'
    os.chdir(prev)

    return

