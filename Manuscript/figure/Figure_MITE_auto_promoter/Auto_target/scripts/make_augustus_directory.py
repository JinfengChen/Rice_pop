#!/usr/bin/env python

import sys
import os
import os.path
import fnmatch

args = sys.argv[1:]

def usage():
    print """Usage: make_augustus_directory.py <sequence_folder> <run_name> <species1> <species2>

This script will generate shell scripts in current directory to submit Augustus jobs to queue for each file in sequence folder. Augustus will use both of the specified trained species. See Augustus for valid species, or do your own training.
"""
    sys.exit(-1)

if (len(args) != 3 and len(args) != 4) or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()

top = '''#!/bin/bash
#PBS -l nodes=1:ppn=1,mem=2gb,walltime=100:00:00 -j oe
module load stajichlab
module load stajichlab-python
module load augustus/2.7

cd $PBS_O_WORKDIR

'''
info = os.listdir(sys.argv[1])
out_handle = open('augustus_all.sh', 'w')
print >> out_handle, top
for i in info:
    if fnmatch.fnmatch(i, '*.fa'):
        fpath = os.path.join(sys.argv[1], i)
        base = os.path.splitext(fpath)[0]
        fbase = os.path.split(base)[1]
        a1_3 = ''
        a3 = ''
        b2 = ''
        full2 = ''
        
        #print fpath
        a1 = "augustus --strand=forward --genemodel=complete --species="
        a1_2 = sys.argv[3] + " " + fpath
        if len(args) == 4:
            a1_3 = sys.argv[4] + " " + fpath
        a2 = a1 + a1_2
        if len(args) == 4:
            a3 = a1 + a1_3
    
            
        base = fpath.split("Length")[0]
        b1 = " > " + base + "_augustus_complete_" + sys.argv[3] + ".gff"
        if len(args) == 4:
            b2 = " > " + base + "_augustus_complete_" + sys.argv[4] + ".gff"
    
        full1 = a2 + b1 
        if len(args) == 4:
            full2 = "\n" + a3 + b2
        whole = full1
        if len(args) == 4:
            whole += full2
        #out_handle = open("augustus-" + sys.argv[2] + "_" + fbase + ".sh", "w")
        print>>out_handle, whole

print>>out_handle, '\n\necho "Done"'
out_handle.close()
    
