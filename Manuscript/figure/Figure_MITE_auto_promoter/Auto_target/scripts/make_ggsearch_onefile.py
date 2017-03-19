#!/usr/bin/env python

import sys
import os
import os.path
import fnmatch

args = sys.argv[1:]

def usage():
    print """Usage: make_glsearch.py <query_sequence_file> <target_sequence_file>

This script will generate shell scripts in current directory to submit ggsearch jobs to queue for each sequence in query sequence file against all sequences in the target sequence file."""
    sys.exit(-1)

if len(args) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()


top = '''#!/bin/bash
#PBS -l nodes=1:ppn=14,walltime=08:00:00 -j oe
module load stajichlab
module load stajichlab-python
module load fasta

cd $PBS_O_WORKDIR

ggsearch36 -T 14 -d 0 -n -E 1E-1 -m 9 '''

base = os.path.splitext(sys.argv[1])[0]
database = os.path.split(os.path.splitext(sys.argv[2])[0])[1]
b1 = " > " + base + "_ggsearch-to_" + database + ".out"
full = top + sys.argv[1] + " " + sys.argv[2] + b1
fbase = os.path.split(os.path.splitext(sys.argv[1])[0])[1]
fbase = fbase.replace(" ", "_").replace(":", "_")
#fbase = fbase[:40]
out_handle = open("ggsearch-" + fbase + "-to_" + database +".sh", "w")
print>>out_handle, full
print>>out_handle, '\n\necho "Done"'
out_handle.close()
