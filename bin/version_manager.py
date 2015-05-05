#!/usr/bin/env python

import subprocess
import os.path
import sys

version_file = 'VERSION'
version_str = None
major_version = None
minor_version = None
build_version = None

def get_version(version_file):
    global version_str
    global major_version
    global minor_version
    global build_version

    if not os.path.isfile(version_file):
        sys.exit(1) 

    f = open (version_file, 'r')
    version_str = f.read().rstrip()
    f.close()
    
    # VERSION - split between major and minor
    major_version = int(version_str.split('.')[0])
    minor_version = int(version_str.split('.')[1])
    
    # BUILD_NUM ?= $(shell git rev-list HEAD --count)
    p = subprocess.Popen(["git", "rev-list", "HEAD", "--count"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    build_version = int(p.stdout.read())

    return

get_version(version_file)
print "'%s' - %s - %s - %s" %(version_str, major_version, minor_version, build_version)
print "VERSION: %s.%s.%s" %(major_version, (minor_version + 1), build_version)

#f = open (file, 'w')
#f.write("%s.%s" %(major_version, minor_version + 1))
