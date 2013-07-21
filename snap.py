import os
import sys
import subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import lib.menu
import lib.term
import lib.box
import lib.dsl
import lib.wentlive
import config

__ORIGINAL_PATH__ = list(sys.path)

def main():

    while True:

        #Restore the original path, in case previous action messed it up
        sys.path = list(__ORIGINAL_PATH__)
        menu = {
                "Snap to a node group": snap_group,
                "Snap to a node":snap_node
               }

        lib.menu.navigate("Choose action",menu)()

        done_menu = {
                        "Return to main menu": "r",
                        "Exit":                "e"
                    }
        next_action = lib.menu.navigate("Snap done, what do?",done_menu,clear_before=False)

        if next_action != "r":
            return

def snap_group():
    groupname,group = lib.menu.navigate("Choose group to snap to",lib.box.groups, depth=0,
                                                                                  selection_also=True)
    snap_project(groupname,group)

def snap_node():
    node = lib.menu.navigate("Choose node to snap to",lib.box.nodes,depth=0)
    snap_project(node.name,[node])

def snap_project(destname,destinations):
    #Choose the project and the branch/tag of it to checkout
    project = lib.menu.navigate("Choose project",lib.box.projects)
    project.choose_and_checkout_branch()

    #If there's a nosnap file we don't actually snap
    nosnap = project.get_nosnap()
    if not nosnap is None:
        print()
        lib.term.print_c(
            "Project has a nosnap file in its root.\nThe contents are:\n",
            lib.term.RED
        )
        print(nosnap)
        return

    #Make sure the user knows what they're doing (never trust the user)
    lib.menu.project_check(project)

    #Create the dsl object, it will house all the ugly state throughout this snap
    pdsl = lib.dsl.dsl(project,destinations)

    #Find the manifest.py file and run it on the dsl object we just created, or
    #run the default manifest on the dsl object if the project doesn't have a
    #manifest
    snap_dir = project.get_snap_dir()
    if os.path.exists(os.path.join(snap_dir,"manifest.py")):
        sys.path.append(snap_dir)
        import manifest
        manifest.run(pdsl)
    else:
        lib.dsl.default_run(pdsl)

    #Tag the snap
    if not pdsl.tagmsg is None:
        lib.menu.header("Tagging project")
        project.tag(pdsl.tagmsg)

    #Send a wentlive
    if pdsl.send_wentlive:
        lib.menu.header("Sending a Wentlive email")
        lib.wentlive.send( project,
                           pdsl.wentlive_src,
                           pdsl.wentlive_dest,
                           destname,
                           config.smtpserver,
                           config.smtplogin,
                           config.smtpssl )

#Run when everything is set up
main()
