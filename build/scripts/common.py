#!/usr/bin/env python

import sys, getopt, commands

verbose = False
domains = ()
dependency_versions_csv_path = ""

def run_command( command ):
    print_verbose(command)
    (exit_code, output) = commands.getstatusoutput(command)
    if exit_code != 0:
        print_error("Exit code: " + str(exit_code))
        print_info(output)
    print_verbose(output)
    return (exit_code, output)


def print_warning(warning):
    print "WARNING: " + warning


def print_error(error):
    print "ERROR: " + error

def print_info(info):
    print info

def print_info_no_eol(info):
    sys.stdout.write(info)

def print_verbose(verbose_info):
    if verbose == True:
        print_info(verbose_info)

def print_verbose_no_eol(verbose_info):
    if verbose == True:
        print_info_no_eol(verbose_info)


def set_flags(argv):
    global verbose
    global domains
    global dependency_versions_csv_path

    usage = 'Usage: ' + __file__ + ' [-hv] [-d <domain1,domain2>] [-f <dependency-versions-file>]'

    try:
        opts, args = getopt.getopt(argv,"hvd:f:", ["help", "verbose", "domains", "dependency-versions-file"])
    except getopt.GetoptError:
        print_error(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_info(usage)
            sys.exit()
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-d', '--domains'):
            domains = arg.split(",")
        elif opt in ('-f', '--dependency-versions-file'):
            dependency_versions_csv_path = arg


if __name__ == '__main__':
    print_error("This module " + __file__ + " cannot be run as a stand alone command")
    sys.exit(1)