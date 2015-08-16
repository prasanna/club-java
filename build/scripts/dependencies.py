#!/usr/bin/env python

import common
import sys
import os.path
import urllib

dependency_versions = {}
messages = []
def validate_dependencies():
    global messages
    load_dependency_versions()
    exit_code = check_for_version_conflicts()
    if exit_code != 0:
        sys.exit(exit_code)

def load_dependency_versions():
    global dependency_versions
    f = open(common.dependency_versions_csv_path, "r")
    raw_dependency_versions = f.read().split("\n")
    raw_dependency_versions.remove("groupId,artifactId,version")
    for raw_dependency_version in raw_dependency_versions:
        dependency_split = raw_dependency_version.split(",")
        if len(dependency_split) == 3:
            dependency_versions[dependency_split[0] + "," + dependency_split[1]] = dependency_split[2]

def check_for_version_conflicts():
    global dependency_versions

    (exit_code, output) = common.run_command("cut -d, -f1-2 " + common.dependency_versions_csv_path + " | sort | uniq -d")

    dups_found = False
    if output != "":
        dups_found = True

    version_conflict_found = False
    (exit_code, output) = common.run_command("sort " + common.dependency_versions_csv_path + " | uniq | cut -d, -f1-2 | uniq -d")
    if output != "":
        version_conflict_found = True

    if version_conflict_found:
        common.print_error("Duplicate dependency with different version numbers definitions found")
        return 1
    elif dups_found:
        common.print_warning("Duplicate dependency definitions found")
    return 0


def dependencies(domain, scope):
    global dependency_versions

    dependency_file = "domains/" + domain + "/src/" + scope + "/java/dependencies.csv"
    dependencies_to_return = {}

    if os.path.isfile(dependency_file):
        f = open(dependency_file, "r")
        deps = f.read().split("\n")
        deps.remove("groupId,artifactId")
        for dep in deps:
            common.print_verbose("Found dependency: " + dep + " with version " + dependency_versions[dep])
            dependencies_to_return[dep] = dependency_versions[dep]

    common.print_verbose(dependencies_to_return)
    return dependencies_to_return


def ensure_ready(domain, scope):
    load_dependency_versions()
    dependency_dir = "domains/" + domain + "/lib/" + scope + "/java/"
    (exit_code, output) = common.run_command("mkdir -p " + dependency_dir)
    deps = dependencies(domain, scope)
    if len(deps) > 0:
        common.print_info("Checking dependencies for " + domain + ": ")
    for dependency, version in deps.iteritems():
        if version != "local":
            (group_id, artifact_id) = dependency.split(",")
            group_id = group_id.replace(".", "/")
            common.print_info_no_eol( "   " + dependency + ": " + version + "... ")
            downloaded_filename = dependency_dir + artifact_id + "-" + version + ".jar"
            dependency_url = "https://search.maven.org/remotecontent?filepath=" + group_id + "/" + artifact_id + "/" + version + "/" + artifact_id + "-" + version + ".jar"
            common.print_verbose('')
            common.print_verbose('URL: ' + dependency_url)
            common.print_verbose('Downloaded filename: ' + downloaded_filename)

            if not os.path.isfile(downloaded_filename):
                urllib.urlretrieve(dependency_url, downloaded_filename)
                common.print_info("downloaded.")
            else:
                common.print_info("exists.")


def classpath_for(domain, scope):
    cp = ""
    to_add = []
    for dependency, version in dependencies(domain, scope).iteritems():
        if version == "local":
            to_add.append("target/domains/main/" + domain)

        else:
            directories_in_classpath = ['domains/' + domain + '/lib/' + scope + '/java/']
            for directory in directories_in_classpath:
                to_add.extend(list_jars_in_directory(directory))

    return add_to_classpath(cp, to_add)


def list_jars_in_directory(directory):
    (exit_code, output) = common.run_command('find ' + directory + ' -name "*.jar" -type f')
    return output.split("\n")


def add_to_classpath(cp, to_add):

    if cp == "":
        cp = ":".join(to_add)
    else:
        cp = cp + ":" + ":".join(to_add)

    common.print_verbose("New classpath: " + cp)
    return cp

def show_dependencies():
    global dependency_versions
    common.print_info("Dependency Versions:")
    for dependency, version in dependency_versions.iteritems():
        common.print_info(dependency + ": " + version)

def main(argv):
    common.set_flags(argv)
    validate_dependencies()
    show_dependencies()


if __name__ == '__main__':
    main(sys.argv[1:])