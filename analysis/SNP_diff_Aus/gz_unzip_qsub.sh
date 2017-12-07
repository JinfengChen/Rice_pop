#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --time=40:00:00
#SBATCH --output=gz_unzip_qsub.sh.%A_%a.stdout
#SBATCH -p intel
#SBATCH --workdir=./

N=$SLURM_ARRAY_TASK_ID
if [ ! $N ]; then
    N=1
fi


FILE=`ls -1 *.gz | head -n $N | tail -n 1`

#tar -zxvf $FILE
gunzip -d $FILE

echo "Done"
