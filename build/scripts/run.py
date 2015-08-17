#!/usr/bin/env python

import sys
import common
import dependencies

def run(runnable_class):
    classpath = dependencies.classpath_for(common.domains[0], common.scopes[0])
    run_command = "java -cp " + classpath + " " + runnable_class
    print common.run_command(run_command)

def main(argv):
    common.set_flags(argv)
    dependencies.load_dependency_versions()
    run(argv[len(argv)-1])

if __name__ == '__main__':
    main(sys.argv[1:])