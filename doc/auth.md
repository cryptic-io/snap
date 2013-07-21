# Authentication

Snap does not have any kind of build-in authentication or permission system. Instead the goal is to
let you use the permission systems of other services to your advantage.

## Git repository access

When cloning a repo snap will use the ssh key of whatever user is currently running snap, so git
access should be configured on the side of the git server against whatever key that happens to be. If
your git service provider (github,bitbucket,etc...) offers the option of cloning https-based git links
and requiring you to input a username and password that is supported as well.

## Remote server access

Once snap has cloned the repository it then carries out commands which involve ssh/rsyncing to remote
boxes and doing things there. At this point there's two ways you could go about controlling access to
who may snap where:

### Centralized access

If your snap setup is located in a central place, and there a few central keys that are used by all
projects by way of their `remote_user_key` parameters in `config.py`, then access should be restricted
by editing the permissions on those central keys to encompass the local users that you want. The best
policy for this case is to have those keys owned by a user which will never actually use snap. This is
because if the user who owns a private key tries to ssh with it, ssh will require that the file has
600 or 400 permissions. If the user ssh-ing doesn't own the key then the only requirement is that they
are able to read the key.

### Distributed access

An alternative setup is to have every user create their own public/private key pair to use when snapping.
If no `remote_user_key` file is specified by the project then snap will use the key of the person
who is doing the snap. This key can then be placed in the `authorized_keys` file of the `remote_user`
on the remote host. This setup is more secure in that it doesn't require multiple users using a single
private key, but it is also more difficult to coordinate on a large-scale setup.
