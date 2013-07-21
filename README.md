# Snap

A code push-deployment tool writtin in python.

## Philosophy

The goal of snap is to make it easy for a codebase to dictate its deployment procedures itself, and
not have that information exist somewhere else (in a chef repo, for instance). Snap reads deployment
procedures from a file inside the repo itself, meaning that the procedure can be easily changed and
tested without leaving the development environment, and can be different on a per-branch basis.

Snap is anti-parallel. This is based on the author's view that parallelism in the snap processes is
sometimes (in the author's experience: often) used to try to beat race-conditions. The problem is that
parallelism doesn't, and will never, solve the problem of race conditions during deployment. Only a
proper deployment procedure can do that. By doing everything single-threaded/serially, snap makes
race-conditions extremely obvious.

## Requirements

The following need to be installed for snap to work:
* Python 3
* git
* rsync
* ssh

## Setup

At this moment snap doesn't need a virtualenv environment to run; it works fine using just default
packages. The setup procedure is:

```bash
git clone https://github.com/cryptic-io/snap.git
cd snap
cp config.py.template config.py
#Edit config.py
```
To run snap simply:

```bash
python snap.py
```

## Usage

Usage is broken down into a few sections:

* [config](doc/config.md)
* [manifest](doc/manifest.md)
* [access control](doc/auth.md)
* [miscellaneous](doc/misc.md)

# Supporters

The following companies/individuals supported the development of snap (and are awesome):

* [Coefficient, Inc](http://www.coefficientinc.com/)

