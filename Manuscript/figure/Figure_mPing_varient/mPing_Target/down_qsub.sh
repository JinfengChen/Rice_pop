#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --time=4:00:00
#SBATCH --output=down_qsub.stdout
#SBATCH -p intel
#SBATCH --workdir=./


CPU=$SLURM_NTASKS
if [ ! $CPU ]; then
   CPU=2
fi

N=$SLURM_ARRAY_TASK_ID
if [ ! $N ]; then
    N=$1
fi

FILE=`cat down.list | head -n $N | tail -n 1`

if [ ! -e $FILE ]; then
    wget $FILE
fi

echo "Done"
