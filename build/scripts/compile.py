#!/usr/bin/env python

import common

def compile(source_dir, target_dir):
    common.run_command('rm -rf ' + target_dir)
    common.run_command('mkdir -p ' + target_dir)
    common.run_command('find ' + source_dir + ' -type f -name "*.java" -print | xargs javac -d ' + target_dir + ' -sourcepath ' + source_dir)



def main(argv):
    number_of_arguments = len(argv)
    if number_of_arguments != 2:
        print_usage()
        sys.exit(1)
    (source_dir, target_dir) = argv
    compile(source_dir, target_dir)

def print_usage():
    print "Usage: compile.py <source_dir> <target_dir>"

if __name__ == '__main__':
    main(sys.argv[1:])