# config.py

`config.py` is a python file which contains configuration information about snap (go figure). There's
two main kinds of items that `config.py` specifies. Keep in mind that `config.py` is a normal python
file, so all configuration can be generated from some other source and simple imported into snap.

## Projects

All projects, or repositories, are specified in `config.py`. For each project it is required that you
specify:

* `name`: The name of the project, can't be the same as the name of any other project.
* `url`: The url of the git repository for the project.
* `location`: The location in the filesystem you want to snap to. This should be an absolute path.

You can also specify:

* `remote_user`: The user you want to own the snapped resources on the remote system. This user must be
                 able to write to the parent of the `location`. This parameter defaults to whatever
                 the name of the local user running snap is.
* `remote_user_key`: The location of the private ssh key to use when snapping. The private ssh key of
                     the local user running snap is used if this isn't specified.

## Nodes

Nodes are other computers that snap can access and push resources to. For each node it is required
that you specify:

* `name`: An identifier for the node. The hostname will do fine.
* `ip`: The ip address or hostname of the node.

You can also specify:

* `ssh_port`: The ssh port to access the node through. Defaults to 22.
* `groups`: A list of strings, each string being the name of a group the node belongs to. When
            snapping you will be given the option of snapping to either an individual node or a group
            of node. This field is what snap uses to consolidate nodes into their respective groups.


