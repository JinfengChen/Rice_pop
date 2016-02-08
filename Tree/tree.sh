#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=10gb
#PBS -l walltime=200:00:00
#PBS -V

cd $PBS_O_WORKDIR

module load treebest
#treebest nj example.maf > example.nhx
#treebest nj test.fasta > test.nhx
treebest nj test.3000.fasta > test.3000.nhx

echo "Done"
