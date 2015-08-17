#!/usr/bin/env python

import sys
import common
import dependencies

def run_tests_for_all(domains, scopes):
    for domain in domains:
        for scope in scopes:
            run_tests_for(domain, scope)

def run_tests_for(domain, scope):
    common.print_info_no_eol("Running " + scope + " for " + domain + "...")
    classpath = dependencies.classpath_for(domain, scope)
    test_classes_as_string = test_classes_for(domain, scope)

    if test_classes_as_string.strip() != "":
        run_tests_command = "java -cp " + classpath + " org.junit.runner.JUnitCore " + test_classes_as_string
        common.print_verbose("Running tests with:")
        common.print_verbose(run_tests_command)
        (exit_code, output) = common.run_command(run_tests_command)
        if exit_code == 0:
            common.print_info(" PASSED.")
        else:
            common.print_info(" FAILED.")
    else:
        common.print_info(" No tests found.")

def test_classes_for(domain, scope):
    test_classes_dir = dependencies.target_dir_for(domain, scope)
    (exit_code, output) = common.run_command("find " + test_classes_dir + " -type f -name *Test.class")
    test_classes = output.split("\n")
    test_classes_as_string = ""
    for test_class in test_classes:
        without_target_dir = test_class.replace(test_classes_dir, "")
        without_class_extn = without_target_dir.replace(".class", "")
        without_leading_slash = without_class_extn.strip("/")
        with_dots_not_slashes = without_leading_slash.replace("/", ".")
        test_classes_as_string = test_classes_as_string + " " + with_dots_not_slashes
    return test_classes_as_string

def main(argv):
    common.set_flags(argv)
    dependencies.load_dependency_versions()
    run_tests_for_all(common.domains, common.scopes)

if __name__ == '__main__':
    main(sys.argv[1:])