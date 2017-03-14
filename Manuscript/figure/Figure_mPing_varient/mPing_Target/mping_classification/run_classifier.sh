#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem=100G
#SBATCH --time=10:00:00
#SBATCH --output=slurm.stdout
#SBATCH -p intel
#SBATCH --workdir=./

#sbatch --array 1 run_speedseq_qsub.sh

module load samtools
PATH=$PATH:~/BigData/software/SVcaller/ROOT/bin/
genome=Fairchild_canu1_3.quiver_round1_pilon.fasta

start=`date +%s`

CPU=$SLURM_NTASKS
if [ ! $CPU ]; then
   CPU=1
fi

python Extract_mPing_varients.py --input rice3k_mPing_target --cpu $CPU


end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"
