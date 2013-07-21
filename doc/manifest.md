# manifest.py

Each project that snap is set up should have a `snap` folder in its root, and in that folder there
should be a file called `manifest.py`. An example `manifest.py` looks like this:

```python
def run(self):
    self.local_script("test1")
    self.stage('.', includes=['foo'], excludes=['bar'])

    cdns = self.get_nodes_in_group("cdn")
    self.stage('.', includes=['foo'], excludes=['bar'], destinations=cdn)

    self.remote_script("test2", destinations=cdns)
```

The `def run(self):` section is required in every manifest. It's needed for snap to have something to
import. The rest of the statements, and more, will be explained next.

### self.get_nodes(nodenames)

This function can be used to return the node objects with the given names. This can be used in
subsequent calls if your deployment procedure requires you to interact with nodes separate from the
main set you chose to snap to in the initial snap process.

### self.get_nodes_in_group(groupname)

This function can be used to return the node objects within the given group name. This can be used in
subsequent calls if your deployment procedure requires you to interact with nodes separate from the
main set you chose to snap to in the initial snap process.

### self.stage(directory, includes=[], excludes=[], destinations=None)

The bread and butter of snap, `stage` is used to actually put files in their remote locations (as
specified by the `location` directive in the project configuration).

`directory` is the directory within the project you want to snap. For instance, if you only want to
snap the directory `imgs` in your project, you would call: `self.stage('imgs/')`, and snap would
synchronize the local `<project root>/imgs` folder with the remote `<location>/imgs` folder.

`includes` and `excludes` are lists of strings which are passed through to rsync. They can be the
names of files, directories, or they can be globs (strings with `*`'s). Includes take precedence over
excludes, so if you wanted to only snap the file `README.md` in the root of your project without
touching anything else you would call `self.snap('.', includes=['README.md'], excludes=['*'])`.

`destinations` is by default `None`, which will cause `stage` to send the files only to the nodes you
chose in the menu leading up to the actual snap. If you want to have a part of your snap process
send files to a different set of nodes, you can pass a list of node objects (obtained through
`self.get_node` or `self.get_nodes_in_group`) here.

The function will return a boolean of whether or not the run was successful.

### self.local_script(scriptname)

This will run a script in the local cache of the project. This script should be located alongside
`manifest.py` in the `snap/` folder in the repository, however the script will be run with the `cwd`
being the root of the repository (the parent of the `snap/` folder). The script will be run as is,
so as long as a shebang line is set the language used does not matter.

The function will return a boolean representing whether the run failed or not. Any output to stderr
by the script will constitute and error.

### self.remote_script(scriptname, destinations=None)

This will run a script on all of the remote machines either in the set chosen in the menu or the ones
in `destinations` (see `self.stage` for more detail on `destinations`). The script should be located
alongside the `manifest.py` in the `snap/` directory in the root of the project, and will be run with
`cwd` being the root of the repository (the parent of the `snap/` folder). The script will be run as
is, so as long as a shebang line is set the language used does not matter.

The function will return a boolean representing whether the run failed or not. Any output to stderr
by the script will constitute and error.

(**NOTE**: This will run whatever is currently present in the remote location. If the first thing your
snap procedure does is run a remote_script, it's possible it won't have the same version as what's in
your local version since you haven't actually pushed any changes yet. If this is the case you should
do a `self.stage('snap/')` before you do this call)

### self.header(string)

Prints out `string` in a nice little header that looks pretty. Has no actual utility other then for
maybe debugging.

### self.navigate(string,menu)

Offer the user doing the snapping a menu. `string` will be used as the title, menu is a dictionary,
where each key is the string which will be shown to the user in the menu selection, and each value is
what the function will return if that key was selected.

If the value is another map, `self.navigate` will call itself on that map instead of returning. In this
way you can have nested menus.

### self.choice(text, default=False)

Presents the user with a yes/no choice. You can pass in whether yes or no should be the default value
(True for yes, False for no). The function returns the corresponding boolean value for the choice.

### self.tag(string)

Set the string you want to tag this snap with. If you set `string` to None then no tagging will take
place. This overwrites whatever is set in `config.py`.

(This statement is delayed, tagging will not take place until the snap is complete, and only one tag
can be done)

### self.wentlive(src=config.wentlive_source, dest=config.wentlive_destination):

Use this to specify that you want to send a wentlive email, and optionally the email the wentlive
should appear to come from (`src`) and where it should go (`dest`, which can be either an email as a
string or a list of email strings). Overwrites whatever is set in `config.py`.

(This statement is delayed, sending of the wentlive will not take place until the snap is complete,
and only one wentlive can be sent out)

### self.no_wentlive()

Use this to specify that no wentlive should be sent. Overwrites whatever is set in `config.py`

### self.get_project_location()

Use this to get the remote directory that snap will use for the project directory (this will be
whatever is specified in `config.py` unless you've changed it with a `self.set_project_location`.

### self.set_project_location(loc)

Use this to set the remote directory that snap will use for the project directory to a different one
than the one specified in `config.py`. Do not include the `testmode_prefix`, that will automatically
be added farther down the pipeline.

# Default manifest

If no `manifest.py` file is found in the `snap/` folder of the project, the default snap procedure
will be used:

```python
def default_run(self):
    self.stage('.')
```


