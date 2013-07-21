import lib.util
import lib.menu
import lib.term
import os
import subprocess
import getpass
import fnmatch

git_env = os.environ.copy()
git_env["GIT_SSH"] = os.path.join(os.getcwd(),"ssh_wrapper.sh")

def cache_path():
    '''Return relative path to repo cache'''
    return os.path.join('.cache','repos')


class project:

    def __init__(self,name,url,location,remote_user=getpass.getuser(),remote_user_key=None):
        self.name     = name
        self.url      = url
        self.location = location
        self.user     = remote_user
        self.key      = remote_user_key
        self.fetched  = False

    def clone(self):
        '''Clones project into cache, unless it's already there'''
        lib.util.mkdir_p(cache_path())
        if not os.path.isdir( os.path.join( self.get_cache_dir(), '.git' ) ):
            lib.term.print_c("Cloning...\n",lib.term.BLUE)
            subprocess.call(["git","clone",self.url],cwd=cache_path(),env=git_env)

    def fetch(self):
        '''Fetches all remote data'''
        self.clone()
        if not self.fetched:
            lib.term.print_c("Fetching....\n",lib.term.BLUE)
            self.fetched = True
            subprocess.call(["git","fetch","-pv","--all"],
                            cwd=self.get_cache_dir(),
                            env=git_env)

    def branches(self):
        '''Lists all current remote braches'''
        self.fetch()
        subprocess.call(["git","remote","prune","origin"],cwd=self.get_cache_dir())
        out = str(subprocess.check_output(["git","branch","-r"],
                                          cwd=self.get_cache_dir(),
                                          env=git_env),'utf8')
        branches = []
        for branch in out.split("\n"):
            if not "HEAD" in branch:
                try:
                    branches.append(branch.split("/")[1])
                except Exception: pass
        return branches

    def tags(self):
        '''List all current tags for the project'''
        subprocess.call(["git","fetch","-pvt","--all"],
                        cwd=self.get_cache_dir(),
                        env=git_env)
        out = str(subprocess.check_output(["git","tag","-l"],cwd=self.get_cache_dir()),'utf8')
        return out.split("\n")

    def current_branch(self):
        '''Returns the name of the current branch'''
        cwd = self.get_cache_dir()
        branch = str(subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"],cwd=cwd),'utf8')
        return branch.rstrip()

    def current_commit(self):
        '''Returns the name of the current commit'''
        cwd = self.get_cache_dir()
        branch = str(subprocess.check_output(["git","rev-parse","HEAD"],cwd=cwd),'utf8')
        return branch.rstrip()

    def current_commit_message(self):
        '''Returns the current commit message'''
        cwd = self.get_cache_dir()
        branch = str(subprocess.check_output(["git","log","-1","--pretty=%B"],cwd=cwd),'utf8')
        return branch.rstrip()

    def checkout(self,branch):
        '''Checks out the given branch in the local cache repo, does a hard reset'''
        self.fetch()
        cwd = self.get_cache_dir()
        lib.term.print_c("Checking out....\n",lib.term.BLUE)
        with open(os.devnull) as null:
            subprocess.call(["git","checkout",branch],stdout=null,stderr=null,cwd=cwd)
            subprocess.call(["git","reset","--hard",branch],cwd=cwd)
            subprocess.call(["git","clean","-f","-d","-x"],cwd=cwd)

    def tag(self,tagname):
        '''Tags whatever commit the project is on and attempts to push that to the remote repo'''
        cwd = self.get_cache_dir()
        subprocess.call(["git","tag",tagname],cwd=cwd)
        subprocess.call(["git","push","--tags"],cwd=cwd)

    def get_cache_dir(self):
        '''Return relative path to project's repo cache'''
        return os.path.join(cache_path(),self.name)

    def get_snap_dir(self):
        '''Returns full path to project's snap directory'''
        return os.path.join(self.get_cache_dir(),"snap")

    def choose_and_checkout_branch(self):
        '''Gives user list of branches to choose from, and checks out the chosen one'''
        branches = {}
        for b in self.branches():
            branches[b] = b
        branches["# Choose a tag instead #"] = True
        branch = lib.menu.navigate("Choose a branch from {0}".format(self.name),branches)

        if branch is True:
            tags = {}
            for t in self.tags():
                if t: tags[t] = t

            if not tags:
                lib.term.big_error("There are no tags associated with this repo\n")
                lib.term.big_error("Press enter to go back\n")
                lib.term.readline()
                return self.choose_and_checkout_branch()

            branch = lib.menu.navigate("Choose a tag from {0}".format(self.name),tags)
        else:
            branch = "origin/"+branch

        self.checkout(branch)
        return branch

    def snap_script(self,script):
        '''Runs a script in the snap directory'''
        cache_path = self.get_cache_dir()
        snap_path  = self.get_snap_dir()
        fn_abs = os.path.join( snap_path, script )
        fn_rel = os.path.join( "snap",    script )
        if os.path.isfile(fn_abs):
            os.system("chmod +x {0}".format(fn_abs))
            lib.util.command_check_stderr([fn_rel], cwd=cache_path)

    def get_nosnap(self):
        '''Returns a nosnap message that exists in the root of the project, or None'''
        cache_path = self.get_cache_dir()
        root_contents = os.listdir(cache_path)
        for f in fnmatch.filter(root_contents,'*.nosnap'):
            fullf = os.path.join(cache_path,f)
            if os.path.isfile(fullf):
                s = ""
                with open(fullf,'r') as fh:
                    for l in fh: s += l
                return s
        return None
