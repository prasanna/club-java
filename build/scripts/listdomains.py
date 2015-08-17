#!/usr/bin/env python

import sys
import common

def find_domains():
    (exit_code, output) = common.run_command('ls -1 domains')
    if exit_code == 0:
        print ",".join(output.split("\n"))

def main(argv):
    common.set_flags(argv)
    find_domains()

if __name__ == '__main__':
    main(sys.argv[1:])