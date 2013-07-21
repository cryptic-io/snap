import sys
import lib.term

def navigate(title,menu,depth=-1,clear_before=True,selection_also=False):
    '''Given a menu title and a dict, has the user navigate the dict as if it was a menu.

    The user is displayed all the keys of the dicts as options, and they can select by
    either option number or by typing in the option name itself. If the selected value
    is valid it is returned, unless it is a dict in which case it is processed as another
    menu.
    '''
    #setup
    menu_numeric = []
    i = 0

    #Sort the menu by key (returns iterable of tuples (key,value))
    menu_sorted = lib.util.dict_sorted(menu)

    #Do the actual printing
    if clear_before: lib.term.clear()
    header(title)
    for (k,v) in menu_sorted:
        print("{0}) {1}".format(i,k))
        menu_numeric.append((k,v))
        i+=1
    lib.term.print_c("\nChoose an option (by number or name): ",lib.term.GREEN)

    #Read and strip the input
    choice = sys.stdin.readline().rstrip()
    print()

    try:
        try:
            #If choice is an integer return from the list
            choice = int(choice)
            (choice,choice_val) = menu_numeric[choice]
        except ValueError:
            #otherwise return from the dict
            choice_val = menu[choice]
    except:
        #If they chose something invalid we'll end up here. Tell them to try again
        lib.term.print_c("Invalid menu choice, try again (hit enter)\n\n",lib.term.RED)
        sys.stdin.readline()
        return navigate(title,menu,depth=depth)

    #If the choice is a dict, do it all again!
    if isinstance(choice_val,dict) and depth != 0:
        return navigate(choice,choice_val,depth-1)
    #Otherwise return our val
    else:
        if selection_also: return choice,choice_val
        else: return choice_val

def header(title,color=lib.term.GREEN):
    '''Prints a pretty header'''
    eq = "="*(len(title)+4)
    lib.term.print_c("\n{0}\n= {1} =\n{0}\n\n".format(eq,title),color)

def project_check(project):
    '''Performs a project check, forcing the user to type in the project name to
    confirm they know what they're doing'''
    header("Are you sure you want to snap {0}?".format(project.name),color=lib.term.RED)
    lib.term.print_c("Type \"{0}\" if you're sure\n".format(project.name),lib.term.RED)
    if lib.term.readline() != project.name:
        lib.term.print_c("\nMistypped, are you sure you chose the right project!\n\n",lib.term.RED)
        project_check(project)


def choice(text,default=False,colors=""):
    '''Gives the user a y/n choice'''
    if default: yn = "[y]/n"
    else: yn = "y/[n]"

    lib.term.print_c("{0} {1} ".format(text,yn),colors)

    answer = lib.term.readline()
    if   answer.lower() == "y": return True
    elif answer.lower() == "n": return False
    else:                       return default
