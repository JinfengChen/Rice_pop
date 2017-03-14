#!/usr/bin/env python

import sys
import os
import fnmatch
import os.path
import time
import subprocess as subp

args = sys.argv[1:]

def usage():
    print """
    usage:
    
    python multi_sub_N_move.py <sh_directory> <match_pattern> <number_to_submit> <folder_to_move_submitted_scripts>
    
    """
    sys.exit(-1)

if len(args) != 4 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()


files = os.listdir(sys.argv[1])
c = 0
for filename in files:
    if fnmatch.fnmatch(filename, sys.argv[2]):
        if c < int(sys.argv[3]):
            #print "This is C before: " + str(c)
            fpath = os.path.join(sys.argv[1], filename)
            subp.call(["qsub", "-q", "highmem", fpath])
            time.sleep(.04)
            subp.call(["mv", "-t", sys.argv[4], fpath])
            time.sleep(.04)
            c += 1
        else:
            exit(0)
