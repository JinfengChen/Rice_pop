#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem=40G
#SBATCH --time=10:00:00
#SBATCH --output=slurm.stdout
#SBATCH -p intel
#SBATCH --workdir=./

module load mafft
module load treebest
module load ncbi-blast/2.2.26

export PATHONPATH=$PATHONPATH:/rhome/cjinfeng/BigData/software/pythonlib/lib/python2.7/site-packages:/rhome/cjinfeng/BigData/software/Target/2.0/
export PATH=$PATH:/rhome/cjinfeng/BigData/software/fasttree/
CPU1=$SLURM_NTASKS
CPU2=1
mode=mi

/rhome/cjinfeng/BigData/software/Target/2.0/target.py -q /rhome/cjinfeng/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query/mping.fa -t nucl -o /rhome/cjinfeng/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target -i $mode -P $CPU1 -C $CPU2 -b_a 12000 -b_d 10 -E -W 5 -f 2 -a flanks -p_M 0.20 -p_n 12000 -p_d 6000 -p_f 5 -S 'MSA' /rhome/cjinfeng/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/rice3k_test4strains.fa Target_Run_mPing_rice3k_test4strains


echo "Done"
