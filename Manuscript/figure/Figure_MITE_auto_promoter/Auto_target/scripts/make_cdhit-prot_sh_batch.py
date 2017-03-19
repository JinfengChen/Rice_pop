#!/usr/bin/env python

import sys
import os
import os.path
import fnmatch

top = '''#!/bin/bash
#PBS -l nodes=1:ppn=8,mem=8gb,walltime=06:00:00
module load stajichlab
module load stajichlab-python

cd-hit-est -i '''

middle = " -o "

bottom2 = " -c 0.9 -G 1 -n 5 -d 0 -g 1 -r 1 -T 24 -M 16000"

in_base = os.path.split(os.path.splitext(sys.argv[1])[0])[1]
base = os.path.splitext(sys.argv[1])[0]

full2 = top + sys.argv[1] + middle + base + "_c90" + bottom2

out_handle2 = open("cd-hit_" + in_base + "-90.sh", "w")
print>>out_handle2, full2
out_handle2.close()
