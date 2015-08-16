#!/usr/bin/env python

import commands
import sys, getopt
import common
import compile
import dependencies


def compile_domains():
    common.print_info("Domains: " + ", ".join(common.domains))
    for domain in common.domains:
        dependencies.ensure_ready(domain, "main")
        print "Compiling " + domain
        compile_by_domain_and_scope(domain, "main")

        dependencies.ensure_ready(domain, "unit-tests")
        compile_by_domain_and_scope(domain, "unit-tests")

def compile_by_domain_and_scope(domain, scope):
    common.print_verbose('Compiling ' + scope)
    compile.compile('domains/' + domain + '/src/' + scope + '/java',
                    'target/domains/' + scope + '/' + domain,
                    dependencies.classpath_for(domain, scope))



def main(argv):
    common.set_flags(argv)

    compile_domains()

if __name__ == '__main__':
    main(sys.argv[1:])