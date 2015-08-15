#!/usr/bin/env python

import sys, commands
import common
import os

def die_if_dups(file_path):
    cwd = os.getcwd()
    full_path = os.path.join(cwd, file_path)
    (exit_code, output) = common.run_command("cut -d, -f1-2 " + full_path + " | sort | uniq -d")

    dups_found = False
    if output != "":
        dups_found = True

    version_conflict_found = False
    (exit_code, output) = common.run_command("sort " + full_path + " | uniq | cut -d, -f1-2 | uniq -d")
    if output != "":
        version_conflict_found = True

    if version_conflict_found:
        common.print_error("Duplicate dependency with different version numbers definitions found")
        sys.exit(1)
    elif dups_found:
        common.print_warning("Duplicate dependency definitions found")


def main(argv):
    number_of_arguments = len(argv)
    if number_of_arguments != 1:
        print_usage()
        sys.exit(1)
    file_path = argv[0]
    die_if_dups(file_path)


def print_usage():
    common.print_error("Usage: dieifdups.py <file>")


if __name__ == '__main__':
    main(sys.argv[1:])
