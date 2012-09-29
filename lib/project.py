import lib.util
import lib.menu
import lib.term
import os
import subprocess

git_env = os.environ.copy()
git_env["GIT_SSH"] = os.path.join(os.getcwd(),"ssh_wrapper.sh")

def cache_path():
    '''Return relative path to repo cache'''
    return os.path.join('.cache','repos')


class project:

    def __init__(self,json):
        self.name    = json["name"]
        self.url     = json["url"]
        self.fetched = False

    def clone(self):
        '''Clones project into cache, unless it's already there'''
        lib.util.mkdir_p(cache_path())
        if not os.path.isdir( os.path.join( self.get_cache_path(), '.git' ) ):
            lib.term.print_c("Cloning...\n",lib.term.BLUE)
            subprocess.call(["git","clone",self.url],cwd=cache_path(),env=git_env)

    def fetch(self):
        '''Fetches all remote data'''
        self.clone()
        if not self.fetched:
            lib.term.print_c("Fetching....\n",lib.term.BLUE)
            self.fetched = True
            subprocess.call(["git","fetch","-v","--all"],
                            cwd=self.get_cache_path(),
                            env=git_env)

    def branches(self):
        '''Lists all current remote braches'''
        self.fetch()
        subprocess.call(["git","remote","prune","origin"],cwd=self.get_cache_path())
        out = str(subprocess.check_output(["git","branch","-r"],
                                          cwd=self.get_cache_path(),
                                          env=git_env),'utf8')
        branches = []
        for branch in out.split("\n"):
            if not "HEAD" in branch:
                try: 
                    branches.append(branch.split("/")[1])
                except Exception: pass
        return branches

    def checkout(self,branch):
        '''Checks out the given branch in the local cache repo, does a hard reset'''
        self.fetch()
        cwd = self.get_cache_path()
        lib.term.print_c("Checking out....\n",lib.term.BLUE)
        with open(os.devnull) as null:
            subprocess.call(["git","branch","-f",branch],stdout=null,stderr=null,cwd=cwd)
            subprocess.call(["git","checkout",branch],stdout=null,stderr=null,cwd=cwd)
            subprocess.call(["git","reset","--hard","origin/"+branch],cwd=cwd)
            subprocess.call(["git","clean","-f","-d"],cwd=cwd)

    def get_cache_path(self):
        '''Return relative path to project's repo cache'''
        return os.path.join(cache_path(),self.name)

    def get_snap_dir(self):
        '''Returns full path to project's snap directory'''
        return os.path.join(self.get_cache_path(),"snap")
        
    def choose_and_checkout_branch(self):
        '''Gives user list of branches to choose from, and checks out the chosen one'''
        branches = {}
        for b in self.branches():
            branches[b] = b
        branch = lib.menu.navigate("Choose a branch from {0}".format(self.name),branches)
        self.checkout(branch)
        return branch

    def get_snapfile_lines(self,fn):
        '''Returns lines from a file in the project's snap directory as a list,
        or empty list on error'''
        lines = []
        try:
            with open(os.path.join(self.get_snap_dir(),fn)) as f:
                for l in f:
                    lines.append(l.rstrip())
            return lines
        except Exception:
            return []

    def get_excludes(self):
        '''Returns project's excludes'''
        return self.get_snapfile_lines("excludes")

    def get_includes(self):
        '''Returns project's includes'''
        return self.get_snapfile_lines("includes")

    def snap_script(self,script):
        '''Runs a script in the snap directory'''
        ps_f = os.path.join(self.get_snap_dir(),script)
        ps_f_rel = os.path.join("snap",script)
        if os.path.isfile(ps_f):
            subprocess.call([ps_f_rel],cwd=self.get_cache_path())

    def post_snap(self):
        '''Run post_snap'''
        self.snap_script("post_snap")

    def get_stages(self):
        stages = []
        i = 1
        lines = self.get_snapfile_lines(str(i))
        while lines != []:
            stages.append({"lines":lines})
            if os.path.isfile(os.path.join(self.get_snap_dir(),"pre_"+str(i))):
                stages[i-1]["pre"] = "pre_"+str(i)
            else:
                stages[i-1]["pre"] = False
            i += 1
            lines = self.get_snapfile_lines(str(i))

        #If the project doesn't have anything defined, just snap everything with no scripts
        if stages == {}:
            return {1:{"lines":["."],"pre":False}}

        return stages

