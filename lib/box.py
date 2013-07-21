import json
import sys
import os
import config

#Init projects
projects = {}
for p in config.projects:
    projects[p.name] = p

#Init nodes and groups from config
nodes = {}
groups = {}
for n in config.nodes:
    nodes[n.name] = n
    for g in n.groups:
        if not g in groups: groups[g] = []
        groups[g].append(n)

def getProject(project):
    '''If it exists, returns project. Else, returns None'''
    if project in projects: return projects[project]
    else: return None

def getNode(node):
    '''If it exists, returns node object. Else, returns None'''
    if node in nodes: return nodes[node]
    else: return None

def getGroup(group):
    '''If it exists, returns group dict. Else, returns empty dict'''
    if group in groups: return groups[group]
    else: return []
