#!/usr/bin/env python

import sys, getopt, commands

verbose = False
domains = ()

def run_command( command ):
    print_verbose(command)
    (exit_code, output) = commands.getstatusoutput(command)
    if exit_code != 0:
        print_error(exit_code)
    print_verbose(output)
    return (exit_code, output)


def print_warning(warning):
    print "WARNING: " + warning


def print_error(error):
    print "ERROR: " + error

def print_info(info):
    print info

def print_verbose(verbose_info):
    if verbose == True:
        print verbose_info

def set_flags(argv):
    global verbose
    global domains

    usage = 'Usage: ' + __file__ + ' [-hv] [-d <domain1,domain2>]'

    try:
        opts, args = getopt.getopt(argv,"hvd:")
    except getopt.GetoptError:
        print_error(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_info(usage)
            sys.exit()
        elif opt in '-v':
            verbose = True
        elif opt in '-d':
            domains = arg.split(",")


if __name__ == '__main__':
    print_error("This module " + __file__ + " cannot be run as a stand alone command")
    sys.exit(1)