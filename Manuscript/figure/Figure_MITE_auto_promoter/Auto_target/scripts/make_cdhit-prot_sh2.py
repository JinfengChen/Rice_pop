#!/usr/bin/env python

import sys
import os
import os.path
import fnmatch
import fastaIO

top = '''#!/bin/bash
#PBS -l nodes=1:ppn=2,walltime=03:00:00
module load stajichlab
module load stajichlab-python
module load cd-hit

python /rhome/bradc/cd-hit_protein_dna2.py '''
c = 1
for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        if fnmatch.fnmatch(filename, '*_fix.dna'):
            fpath = os.path.join(root, filename)
            if os.stat(fpath).st_size == 0:
                continue
            in_handle = open(fpath, "r")
            d = 0
            for title, seq in fastaIO.FastaGeneralIterator(in_handle):
                d += 1
            in_handle.close()
            if d < 2:
                continue
            full = top + root
            out_handle = open(sys.argv[2] + str(c) + ".sh", "w")
            print>>out_handle, full
            out_handle.close()
            c += 1
