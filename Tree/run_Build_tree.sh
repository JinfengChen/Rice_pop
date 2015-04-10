#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l walltime=100:00:00
#PBS -V

#qsub -q js run_Build_tree.sh 
cd $PBS_O_WORKDIR

python Build_Tree.py --fasta test.3000.fasta

echo "Done"
