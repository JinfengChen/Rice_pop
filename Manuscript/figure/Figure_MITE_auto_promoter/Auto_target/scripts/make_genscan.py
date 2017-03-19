#!/usr/bin/env python

import sys
import os
import os.path
import fnmatch

args = sys.argv[1:]


def usage():
    print """
    usage:
    
    python make_genscan.py <DNA_sequences_folder> <match_pattern> <species_matrix>
    
    This script will generate .sh scripts for job submission to run genscan using the indicated matrix for every sequence file matching the match pattern in the specified folder. There are three species that have a matrix: Arabidopsis, Maize, and 
    human.
    """
    sys.exit(-1)

if len(args) != 3 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()    
    

top = '''#!/bin/bash
#PBS -l nodes=1:ppn=1,mem=2gb,walltime=100:00:00 -j oe

cd $PBS_O_WORKDIR

'''
if sys.argv[3] == 'arabidopsis' or sys.argv[3] == 'Arabidopsis':
    model = 'Arabidopsis.smat'
    name = 'arab'
elif sys.argv[3] == 'maize' or sys.argv[3] == 'Maize':
    model = 'Maize.smat'
    name = 'maize'
else:
    model = 'HumanIso.smat'
    name = 'human'

middle = model + ''' '''

files = os.listdir(sys.argv[1])
out_handle = open("genscan_all.sh", 'w')
print >> out_handle, top
for item in files:
    if fnmatch.fnmatch(item, sys.argv[2]):
        fpath = os.path.join(sys.argv[1], item)
        base = os.path.splitext(fpath)[0]
        b1 = " > " + base + "_" + name + "_genscan.out"
        full1 = '/rhome/cjinfeng/BigData/00.RD/Mosquito_TE/Autonomous/Genscan/genscan /rhome/cjinfeng/BigData/00.RD/Mosquito_TE/Autonomous/Genscan/' + middle + fpath + b1 
    
        root, filename = os.path.split(item)
        fbase = os.path.splitext(filename)[0]
        fbase = fbase.replace(" ", "_").replace(":", "_")
        fbase = fbase[:60]
        #out_handle = open("genscan-" + name + "_" + fbase + ".sh", "w")
        print>>out_handle, full1
print >> out_handle, '\n\necho "Done"'        
out_handle.close()
    
