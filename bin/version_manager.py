#!/usr/bin/env python

from optparse import OptionParser
import subprocess
import os.path
import sys

version_file = 'VERSION'
major_version = None
minor_version = None
patch_version = None

#===============================================================================
#                               Options Parser
#===============================================================================

parser = OptionParser()
parser.add_option("-f", "--file", dest="version_file", 
        help="A VERSION file to read (DEFAULT: ./VERSION)")
parser.add_option("--uprev-major", action="store_true", dest="uprev_major", default=False, 
        help="This uprevs the MAJOR version number")
parser.add_option("--uprev-minor", action="store_true", dest="uprev_minor", default=False, 
        help="This uprevs the MINOR version number")
parser.add_option("--uprev-patch", action="store_true", dest="uprev_patch", default=False, 
        help="This uprevs the PATCH version number")
parser.add_option("--write-patch", action="store_true", dest="write_patch", default=False, 
        help="This toggles writing the patch number to the VERSION file (Default: False)")
(option, args) = parser.parse_args()


#===============================================================================
#                               Utility Functions
#===============================================================================


def get_version(version_file):
    global parser
    global major_version
    global minor_version
    global patch_version

    if not os.path.isfile(version_file):
        print "[ERROR] %s does not exist!\n" %(version_file)
        parser.print_help()
        sys.exit(1) 

    f = open (version_file, 'r')
    version_str = f.read().rstrip()
    f.close()
    
    # VERSION - split between major, minor, and patch (if it exists)
    version_list = version_str.split('.')
    major_version = int(version_list[0])
    minor_version = int(version_list[1])
    
    if len(version_list) > 2:
        # Use the patch number in the VERSION file
        patch_version = int(version_list[2])
    else:
        # BUILD_NUM ?= $(shell git rev-list HEAD --count)
        p = subprocess.Popen(["git", "rev-list", "HEAD", "--count"]
                , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        patch_version = int(p.stdout.read())

    return

def write_version(version_file, major, minor, patch, write_version=False):
    f = open (version_file, 'w')
    if write_version:
        f.write("%s.%s.%s" %(major, minor, patch))
    else:
        f.write("%s.%s" %(major, minor))

    return


#===============================================================================
#                                   Main
#===============================================================================


version_file = option.version_file if option.version_file else version_file
get_version(version_file)

if option.uprev_major:
    major_version += 1
    minor_version = 0
    patch_version = 0
elif option.uprev_minor:
    minor_version += 1
    patch_version = 0
elif option.uprev_patch:
    patch_version += 1

if option.uprev_major or option.uprev_minor or option.uprev_patch:
    write_version(version_file, major_version, minor_version, patch_version, option.write_patch)

print "VERSION: %s.%s.%s" %(major_version, minor_version, patch_version)
