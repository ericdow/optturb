import os, string, fileinput

in_file = 'ifDual_channel.in'
out_file = 'ifDual.out'

def runadj(path, restart, nsteps):

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
        if line[0:2] == 'CONVERGE_TOL':
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
    open(in_file,'w').writelines(lines)

    '''
    # change the restart file that will be used
    rep = 'RESTART = '
    rep += restart
    lines = open(in_file,'r').readlines()
    i = 0
    for line in lines:
        if line[0:6] == 'RESTART':
            del lines[i]
        i+=1
    lines.append(rep)

    # change number of steps and timestep
    rep = 'NSTEPS = '
    rep += str(nsteps)
    rep += '\n'
    lines = open(in_file,'r').readlines()
    i = 0
    for line in lines:
        if line[0:6] == 'NSTEPS':
            del lines[i]
        if line[0:1] == 'DT':
            del lines[i]
        i+=1
    lines.append(rep)
    rep = 'DT = 0.0025'
    lines.append(rep)
    open(in_file,'w').writelines(lines)
    '''

    # call ifDual...
    cmd = '/home/ericdow/code/ttadj/ifDualAdj 2 > '
    cmd += out_file
    print ''.join(['Running Adjoint from ',restart,'...'])
    os.system(cmd)
    print 'Done running Adjoint'
    os.chdir(prev)

    return

def runpri(path, restart, nsteps):

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
        if line[0:2] == 'CONVERGE_TOL':
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
    open(in_file,'w').writelines(lines)

    # call ifDual...
    cmd = '/home/ericdow/code/ttadj/ifDualAdj 0 > '
    cmd += out_file
    print ''.join(['Running Primal from ',restart,'...'])
    os.system(cmd)
    print 'Done running Primal'
    os.chdir(prev)

    return

