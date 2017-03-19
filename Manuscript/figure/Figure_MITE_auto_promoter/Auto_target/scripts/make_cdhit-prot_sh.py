#!/usr/bin/env python

import sys
import os
import os.path
import fnmatch

top = '''#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=40G
#SBATCH --time=10:00:00
#SBATCH --output=slurm.stdout
#SBATCH -p intel
#SBATCH --workdir=./

module load cd-hit/4.6.4

cd-hit-est -i '''

middle = " -o "

bottom1 = " -c 0.8 -G 1 -n 3 -d 0 -g 1 -r 1 -T 24 -M 16000"
bottom2 = " -c 0.9 -G 1 -n 5 -d 0 -g 1 -r 1 -T 24 -M 16000"

in_base = os.path.split(os.path.splitext(sys.argv[1])[0])[1]
base = os.path.splitext(sys.argv[1])[0]
full1 = top + sys.argv[1] + middle + base + "_c80" + bottom1
full2 = top + sys.argv[1] + middle + base + "_c90" + bottom2

out_handle1 = open("cd-hit_" + in_base + "-80.sh", "w")
out_handle2 = open("cd-hit_" + in_base + "-90.sh", "w")
print>>out_handle1, full1
print>>out_handle2, full2
print>>out_handle2, '\n\necho "Done"'
out_handle1.close()
out_handle2.close()
