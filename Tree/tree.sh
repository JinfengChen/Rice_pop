#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=2gb
#PBS -l walltime=100:00:00
#PBS -V

cd $PBS_O_WORKDIR

module load treebest
#treebest nj example.maf > example.nhx
treebest nj test.fasta > test.nhx

echo "Done"
