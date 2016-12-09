#!/usr/bin/env python

import common
import sys
import os.path, time
import urllib
import xml.etree.cElementTree as xml

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
    deps = direct_dependencies(domain, scope)
    return deps

def direct_dependencies(domain, scope):
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
    deps = dependencies(domain, scope)
    if len(deps) > 0:
        common.print_info("Checking dependencies for " + domain + ": ")
    for dependency, version in deps.iteritems():
        if version != "local":
            (group_id, artifact_id) = dependency.split(",")
            d = Dependency(domain, scope, group_id, artifact_id, version)

            d.recursive_fetch()


def classpath_for(domain, scope):
    cp = ""
    to_add = []
    for dependency, version in dependencies(domain, scope).iteritems():
        if version == "local":
            (g, a) = dependency.split(",")
            (d, s) = a.split("-")
            to_add.append(target_dir_for(d, s))

        else:
            directories_in_classpath = ['domains/' + domain + '/lib/' + scope + '/jar/']
            for directory in directories_in_classpath:
                to_add.extend(list_jars_in_directory(directory))

    to_add.append(target_dir_for(domain, scope))

    return add_to_classpath(cp, to_add)


def target_dir_for(domain, scope):
    return "target/domains/" + scope + "/" + domain

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


class Dependency:
    def __init__(self, domain, scope, group_id, artifact_id, version):
        self.domain = domain
        self.scope = scope
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version

    def islocal(self):
        return self.version == "local"

    def islatest(self):
        return os.path.isfile(self.locallocation("jar"))

    def verify(self):
        dependencies_last_modified = os.path.getmtime(common.dependency_versions_csv_path)
        local_jar_last_modified = os.path.getmtime(self.locallocation("jar"))
        local_pom_last_modified = os.path.getmtime(self.locallocation("pom"))
        local_jarasc_last_modified = os.path.getmtime(self.locallocation("jar.asc"))
        local_pomasc_last_modified = os.path.getmtime(self.locallocation("pom.asc"))

    def recursive_fetch(self):
        self.fetch()
        for dep, version in self.dependencies().iteritems():
            group_id, artifact_id = dep.split(",")
            d = Dependency(self.domain, self.scope, group_id, artifact_id, version)
            d.recursive_fetch()

    def fetch(self):
        common.print_info_no_eol( "   " + self.group_id + "," + self.artifact_id + ": " + self.version + "... ")

        common.print_verbose('')
        common.print_verbose('URL: ' + self.remotelocation("jar"))
        common.print_verbose('Local: ' + self.locallocation("jar"))

        if not self.islatest():
            self.forcefetch("jar")
            self.forcefetch("pom")
            self.forcefetch("pom.asc")
            self.forcefetch("jar.asc")
            common.print_info("downloaded")
        else:
            common.print_info("exists")

    def forcefetch(self, type):
        common.run_command("mkdir -p " + self.localdir(type))
        urllib.urlretrieve(self.remotelocation(type), self.locallocation(type))

    def localdir(self, type):
        return "domains/" + self.domain + "/lib/" + self.scope + "/" + type

    def locallocation(self, type):
        return self.localdir(type) + "/" + self.artifact_id + "-" + self.version + "." + type

    def remotelocation(self, type):
        group_id_with_dots = self.group_id.replace(".", "/")
        dependency_url = "https://search.maven.org/remotecontent?filepath=" + group_id_with_dots + "/" + self.artifact_id + "/" + self.version + "/" + self.artifact_id + "-" + self.version + "." + type
        return dependency_url

    def dependencies(self):
        pom = Pom(self.locallocation("pom"))
        return pom.direct_dependencies

class Pom:
    def __init__(self, pom_location):
        self.direct_dependencies = {}
        self.parse(pom_location)

    def parse(self, pom_location):
        pom = xml.parse(pom_location)

        in_plugins = False

        for elem in pom.iter():
            if(elem.tag == "{http://maven.apache.org/POM/4.0.0}plugins"):
                in_plugins = True

            if(in_plugins and elem.tag == "plugins"):
                in_plugins = False

            if(not in_plugins and elem.tag == "{http://maven.apache.org/POM/4.0.0}dependencies"):

                for dep in elem.findall("{http://maven.apache.org/POM/4.0.0}dependency"):
                    group_id = dep.find("{http://maven.apache.org/POM/4.0.0}groupId").text
                    artifact_id = dep.find("{http://maven.apache.org/POM/4.0.0}artifactId").text
                    version = get_text(dep.find("{http://maven.apache.org/POM/4.0.0}version"))
                    self.direct_dependencies[group_id + "," + artifact_id] = version
                    common.print_info("        " + group_id + ", " + artifact_id + ", " + version)
                    group_id = artifact_id = version = ""



def get_text(elem):
    if elem is None:
      return ""
    return elem.text


def main(argv):
    common.set_flags(argv)
    validate_dependencies()
    show_dependencies()

if __name__ == '__main__':
    main(sys.argv[1:])
