#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=20G
#SBATCH --time=4:00:00
#SBATCH --output=stdout
#SBATCH -p batch
#SBATCH --workdir=./


ref=mPing_flanking_1000_plus.fa
dict=mPing_flanking_1000_plus.dict

module load samtools
module load picard

picard CreateSequenceDictionary R=$ref O=$dict
samtools faidx $ref

echo "Done"

