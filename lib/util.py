import os
import errno
import subprocess

def mkdir_p(path):
    '''Recursively make all directories in a path'''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def dict_sorted(d):
    '''Returns dict sorted by key as a list of tuples'''
    return sorted(d.items(), key=lambda x: x[0])

def command_check_stderr(command,cwd="."):
    '''Performs a command, piping out both stdout and stderr. If anything comes out
    on stderr it will throw an exception'''
    proc = subprocess.Popen(command, cwd=cwd,
                            stdout=None, # print to terminal
                            stderr=subprocess.PIPE)
    dup  = subprocess.Popen(["tee","/dev/stderr"], stdin=proc.stderr,
                            stdout=subprocess.PIPE, # catch errors from first
                            stderr=None) # also print them to terminal
    errors = str(dup.stdout.read(),'utf8')

    if errors:
        raise Exception("There were errors running {0}:\n{1}".format(command,errors))
