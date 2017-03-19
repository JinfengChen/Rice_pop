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
    Usage: make_activeTE-pep-msa.py <pep-cluster_MSA_folder> <match_pattern> <run_name> <found_superfamily_list>

    
    """
    sys.exit(-1)

if (len(args) != 3 and len(args) != 4) or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()


top = '''#!/bin/bash
#!/bin/bash
#PBS -l nodes=1:ppn=1,mem=8gb,walltime=08:00:00 -j oe
module load stajichlab
module load perl/5.16.3
module load fasta
module load trimal

cd $PBS_O_WORKDIR

perl /rhome/cjinfeng/software/tools/mTEA/scripts/activeTE_msa.pl -p -a -f 26 '''

files = os.listdir(sys.argv[1])
for i in files:
    if fnmatch.fnmatch(i, sys.argv[2]):
        fpath = os.path.join(sys.argv[1], i)
        if len(args) == 4:
            full = top + fpath + " " + sys.argv[4]
        else:
            full = top + fpath
        out_handle = open("aTE-pep_" + sys.argv[3] + "_" + i + ".sh", "w")
        print>>out_handle, full
        out_handle.close()
            

