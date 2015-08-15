#!/usr/bin/env python

import commands
import sys, getopt
import common
import compile


def compile_domains():
    common.print_info("Domains: " + ", ".join(common.domains))
    for domain in common.domains:
        print "Compiling " + domain
        compile_main(domain)
        compile_unit_tests(domain)

def compile_main(domain):
    common.print_verbose("Compiling main")
    compile.compile('domains/' + domain + '/src/main/java', 'target/domains/main/' + domain)

def compile_unit_tests(domain):
    common.print_verbose("Compiling unit-tests")
    compile.compile('domains/' + domain + '/src/unit-tests/java', 'target/domains/unit-tests/' + domain)

def main(argv):
    common.set_flags(argv)

    compile_domains()

if __name__ == '__main__':
    main(sys.argv[1:])