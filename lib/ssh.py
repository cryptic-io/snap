import os
import config
from lib.util import command_check_stderr
import getpass

def ssh(node,command,cwd="/tmp",user=getpass.getuser(),key=None):
    '''ssh's into a node and runs command, cd-ing into cwd first'''

    ssh_command = "cd {0} && {1}".format(cwd,command)
    command =  ["ssh","-t","-q","-p",str(node.ssh_port)]
    if key: command += [ "-i",key]
    command += ["{0}@{1}".format(user,node.ip),ssh_command]
    print(str.join(" ",command[:-1])+" '{0}'".format(ssh_command))

    command_check_stderr(command)

def ssh_project(node,project,command):
    '''Same as ssh, but cwds into a project's directory first'''
    project_path = project.location
    if config.testmode: project_path = config.testmode_prefix+project_path

    user = getpass.getuser()
    if project.user:
        user = project.user

    key = None
    if project.key:
        key = project.key

    ssh(node,command,cwd=project_path,user=user,key=key)
