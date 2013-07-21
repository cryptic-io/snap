import sys

RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
PURPLE = "\033[35m"
CYAN   = "\033[36m"
WHITE  = "\033[37m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def print_c(text,colors):
    '''Prints a string with the given colors

    Example: print_c("hello world",RED+BOLD)
    '''
    sys.stdout.write(colors+text+RESET)
    sys.stdout.flush()

def error(text):
    '''Print out an error'''
    print_c(text,RED)

def big_error(text):
    '''Print out an error with more gusto'''
    print_c(text,RED+BOLD)

def clear():
    '''Clears terminal'''
    print(chr(27)+chr(91)+'H'+chr(27)+chr(91)+'J')

def readline():
    '''Reads a line in from the user and strips out the newline'''
    return sys.stdin.readline().rstrip()

def blockread():
    '''Reads in multiple lines from the user until the user enters a blank
    line. Returns the full string of what was input, sans the final newline'''
    lines = []
    while True:
        line = readline()
        if line:
            lines.append(line)
        else:
            break
    return "\n".join(lines)+"\n"
