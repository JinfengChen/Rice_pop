#!/usr/bin/env python

import sys
import os
import re
import fnmatch
import os.path
import subprocess as subp
import fastaIO
import glob
import fnmatch

args = sys.argv[1:]

def usage():
    print """
    usage:
    
    python make_target_nonauto_general.py <nonauto_queries_folder> <output_folder> <genome_file> <run_name>
    
    """
    sys.exit(-1)

if len(args) != 4 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()

files = os.listdir(sys.argv[1])

top = '''#!/bin/bash
#PBS -l nodes=1:ppn=16,mem=16g
#PBS -l walltime=100:00:00
module load stajichlab
module load stajichlab-python
module load mafft
module load FastTree
module load treebest
module load target

cd $PBS_O_WORKDIR
CPU1=1
CPU2=16
mode=mi

/rhome/cjinfeng/software/tools/Target/2.0/target.py -q '''

middle = ''' -t nucl -o '''

bottom = ''' -i $mode -P $CPU1 -C $CPU2 -b_a 12000 -DB -b_d 10 -E -W 5 -f 1.2 -a flanks -p_M 0.40 -p_n 12000 -p_d 6000 -p_f 100 '''

if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])

for item in files:
    short_name = os.path.splitext(item)[0]
    fpath = os.path.join(sys.argv[1], item)
    if len(short_name) >= 60:
        short_name = short_name[:60]
    
    full = top + fpath + middle + sys.argv[2] + bottom + sys.argv[3] + ' '  + sys.argv[4]
    out_handle = open(sys.argv[4] + '_' + short_name + ".sh", "w")
    print>>out_handle, full
    print>>out_handle, '\n\necho "Done"'
    out_handle.close()
