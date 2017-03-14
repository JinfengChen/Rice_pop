#!/usr/bin/env python

import sys
import os
import fnmatch
import os.path
import subprocess as subp
import fastaIO


args = sys.argv[1:]

def usage():
    print """
    usage:
    
    python make_activeTE_sh.py <nonauto_msa_folder> <match_pattern> <run_name> <found_TPase_file(optional)>
    
    """
    sys.exit(-1)

if (len(args) != 3 and len(args) != 4) or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()


top = '''#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=3gb
#PBS -l walltime=02:00:00
#PBS -j oe

module load stajichlab
module load perl/5.16.3
module load trimal
module load fasta

cd $PBS_O_WORKDIR

'''

bottom = '''
perl /rhome/cjinfeng/software/tools/mTEA/scripts/activeTE_msa.pl -a '''


files = os.listdir(sys.argv[1])
for filename in files:
    if fnmatch.fnmatch(filename, sys.argv[2]):
        path = os.path.abspath(os.path.join(sys.argv[1], filename))
        short = os.path.split(os.path.splitext(path)[0])[1]
        if "_TSD_" in short:
            short = short.replace("_TSD_", "_")
        if "-rice" in short:
            short = short.replace("-rice", "")
        if "-Rice" in short:
            short = short.replace("-Rice", "")
        #path = path.replace("/bigdata/bradc/ae/","")
        if len(args) == 4:
            full = top + bottom + path + " " + sys.argv[3]
        else:
            full = top + bottom + path
        
        out_handle = open("aTE-" + sys.argv[3] + "_" + short + ".sh", "w")
        print>>out_handle, full
        print >>out_handle, '\n\necho "Done"'
        out_handle.close()
            

