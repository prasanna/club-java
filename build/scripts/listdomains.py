#!/usr/bin/env python

import sys, commands
import common

def find_domains():
    (exit_code, output) = commands.getstatusoutput('ls -1 domains')
    if exit_code == 0:
        print ",".join(output.split("\n"))


def main(argv):
    common.set_flags(argv)
    find_domains()

if __name__ == '__main__':
    main(sys.argv[1:])