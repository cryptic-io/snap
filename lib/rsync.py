import config
import os
import subprocess
from lib.util import command_check_stderr

def rsync(project,node,files='.',includes=None,excludes=None):
    '''Runs the rsync command on project, rsyncing it to node'''
    if includes is None: includes = []
    if excludes is None: excludes = []

    excludes_opts = []
    for e in excludes:
        excludes_opts.append("--exclude={0}".format(e))

    includes_opts = []
    for i in includes:
        includes_opts.append("--include={0}".format(i))

    local_project_files  = os.path.join(project.get_cache_dir(),files)
    remote_project_path  = project.location
    if config.testmode: remote_project_path = config.testmode_prefix+remote_project_path

    key_stmt = ""
    if project.key:
        key_stmt = "-i {0}".format(os.path.join(os.getcwd(),project.key))

    command  = ["rsync", "-av", "--delete"]
    command += excludes_opts
    command += includes_opts
    command += ["-e",'/usr/bin/ssh {0} -p{1}'.format(key_stmt,str(node.ssh_port))]
    command += ["--rsync-path=mkdir -p {0} && rsync".format(remote_project_path)]
    command += [local_project_files]
    command += ["{0}@{1}:{2}".format(project.user,node.ip,remote_project_path)]

    print(command)

    command_check_stderr(command)
