#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=10gb
#PBS -l walltime=100:00:00
#PBS -V

cd $PBS_O_WORKDIR

python Remove_Corrected_SNP.py

echo "Done"
