#!/usr/bin/env python

import common
import sys

def compile(source_dir, target_dir, classpath):
    cp_string = ""
    if classpath != "":
        cp_string = " -cp " + classpath + " "

    common.run_command('rm -rf ' + target_dir)
    common.run_command('mkdir -p ' + target_dir)
    common.run_command('find ' + source_dir + ' -type f -name "*.java" -print | xargs javac ' + cp_string + ' -d ' + target_dir + ' -sourcepath ' + source_dir)



def main(argv):
    number_of_arguments = len(argv)
    if number_of_arguments != 3:
        print_usage()
        sys.exit(1)
    (source_dir, target_dir, classpath) = argv
    compile(source_dir, target_dir, classpath)

def print_usage():
    print "Usage: compile.py <source_dir> <target_dir> <classpath>"

if __name__ == '__main__':
    main(sys.argv[1:])