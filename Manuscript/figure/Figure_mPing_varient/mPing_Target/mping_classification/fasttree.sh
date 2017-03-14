#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --time=4:00:00
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
   CPU=2
fi

/rhome/cjinfeng/BigData/software/fasttree/FastTree -noml -nome -nt rice3k_mPing_target.mPing.clean.Nclean.name.blast.table.representive.mPing_var.msa > rice3k_mPing_target.mPing.clean.Nclean.name.blast.table.representive.mPing_var.tree

end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"
