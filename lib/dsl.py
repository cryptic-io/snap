import config
import lib.rsync
import lib.menu
import lib.ssh
import lib.box

def default_run(self):
    self.stage('.')

class dsl:

    def __init__(self,project,destinations):
        '''Initialize the state for a single snap'''
        self.project = project
        self.destinations = destinations
        self.tagmsg = config.default_tag(project)
        self.send_wentlive = config.wentlive_always
        self.wentlive_src = config.wentlive_source
        self.wentlive_dest = config.wentlive_destination

    def stage(self,stage,includes=None,excludes=None,destinations=None):
        '''stage snaps the directory specified by the "stage" arguement to the
        corresponding directory on the remote servers. Includes and excludes can
        be specified, and the remote servers being snapped to can be overwritten'''
        if includes is None: includes = []
        if excludes is None: excludes = []
        if destinations is None: destinations = self.destinations

        for e in config.default_excludes:
            excludes.append(e)

        for node in destinations:
            lib.menu.header("Snapping {0} to {1}".format(stage,node.name))
            try:
                lib.rsync.rsync(self.project,node,stage,includes,excludes)
            except Exception as e:
                lib.term.big_error(str(e))
                return False
        return True

    def local_script(self,script):
        '''Runs script locally, assuming it exists in the project's snap directory'''
        lib.menu.header("Running {0} locally".format(script))
        try:
            self.project.snap_script(script)
        except Exception as e:
            lib.term.big_error(str(e))
            return False
        return True

    def remote_script(self,script,destinations=None):
        '''Runs script remotely, assuming it exists in the project's snap directory.
        Servers the script is run on can be overwritten'''
        if destinations is None: destinations = self.destinations
        for node in destinations:
            lib.menu.header("Running {0} script on {1}".format(script,node.name))
            try:
                lib.ssh.ssh_project(node,self.project,"chmod +x snap/{0} && snap/{0}".format(script))
            except Exception as e:
                lib.term.big_error(str(e))
                return False
        return True

    def header(self,title):
        '''Prints a pretty header'''
        return lib.menu.header(title,lib.term.BLUE)

    def navigate(self,title,menu):
        '''Presents the user with a menu'''
        return lib.menu.navigate(title,menu,clear_before=False)

    def choice(self,text,default=False):
        '''Gives the user free choice. Robots are so jelly'''
        return lib.menu.choice(text,default,lib.term.BLUE)

    def get_nodes(self,nodes):
        '''Returns the node objects with the given node names'''
        ret = []
        for n in nodes:
            ret.append(lib.box.getNode(n))
        return ret

    def get_nodes_in_group(self,group):
        '''Returns the node objects in the given group'''
        return lib.box.getGroup(group)

    def tag(self,msg):
        '''Records that we want to tag the snap with the given snap message'''
        self.tagmsg = msg

    def wentlive(self,src=config.wentlive_source,dest=config.wentlive_destination):
        '''Records that we want to send a wentlive and optionally overwrites source
        and destination of said wentlive'''
        self.send_wentlive = True
        self.wentlive_src = src
        self.wentlive_dest = dest

    def no_wentlive(self):
        '''Records that we don't want to send a wentlive'''
        self.send_wentlive = False

    def get_project_location(self):
        '''Returns the directory that the project is currently set to snap to'''
        return self.project.location

    def set_project_location(self,loc):
        '''Sets the directory that the project will snap to'''
        self.project.location = loc
