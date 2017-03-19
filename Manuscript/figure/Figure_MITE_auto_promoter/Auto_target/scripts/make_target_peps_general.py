#!/usr/bin/env python

import sys
import os
import os.path
import glob


args = sys.argv[1:]

def usage():
    print """
    python make_target_peps_general.py <protein_queries_folder> <output_folder> <genome_file> <run_name>

    example:

    python make_target_peps_general.py /shared/stajichlab/projects/mosquito/target/in/aa_classII/ /shared/stajichlab/projects/mosquito/target/out/fungi/Leucoagaricus/peps/ /shared/stajichlab/projects/mosquito/target/genomes/Leucoagaricus_strain1.ALLPATHS_2.fasta leu-aa
    """
    sys.exit(-1)

if len(args) != 4 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()


files = os.listdir(sys.argv[1])

top = '''#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem=40G
#SBATCH --time=10:00:00
#SBATCH --output=slurm.stdout
#SBATCH -p intel
#SBATCH --workdir=./

module load mafft
module load treebest
module load fasttree/2.1.8
module load ncbi-blast/2.2.26

CPU1=$SLURM_NTASKS
CPU2=1
mode=g
stop=PHI
/rhome/cjinfeng/BigData/software/Target/brad/TARGeT/target.py -q '''

middle = ''' -t prot -o '''

bottom = ''' -i $mode -DB -P $CPU1 -b_e 0.1 -b_a 10000 -S $stop -b_d 20 -p_e 0.1 -p_M 0.35 -p_n 10000 -p_d 10000 -p_f 10000 '''

for item in files:
    short_name = os.path.splitext(item)[0]
    if ".fa" in short_name:
        short_name = short_name.replace(".fa", "_")
    if ".fasta" in short_name:
        short_name = short_name.replace(".fasta", "_")
    if len(short_name) >= 60:
        short_name = short_name[:60]
    full = top + os.path.join(sys.argv[1], item) + middle + sys.argv[2] + bottom + sys.argv[3] + ' ' + sys.argv[4] + '_' + short_name
    out_handle = open(sys.argv[4] + '_' + short_name + ".sh", "w")
    print>>out_handle, full
    print>>out_handle, '\n\necho "Done"'
    out_handle.close()
    #os.system('bash %s' %(sys.argv[4] + '_' + short_name + ".sh"))
