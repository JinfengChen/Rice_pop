#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --mem=30G
#SBATCH --time=4:00:00
#SBATCH --output=run_ADMIXTURE.sh.%A_%a.stdout
#SBATCH -p intel
#SBATCH --workdir=./



start=`date +%s`

CPU=$SLURM_NTASKS
if [ ! $CPU ]; then
   CPU=2
fi

N=$SLURM_ARRAY_TASK_ID
if [ ! $N ]; then
    N=1
fi

echo "CPU: $CPU"
echo "N: $N"

admixture=/rhome/cjinfeng/BigData/software/ADMIXTURE/admixture_linux-1.3.0/admixture

#reorder Qmatrix
python Reorder_Q.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.$N\.Q --reorder_list 3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.tip.label.txt
#defined color for each cluster based on predefined color
python Summary_Cluster_Color.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.$N\.Q

#python $faststruct/structure.py -K $N --input=core_v0.7.pruneddata --output=testoutput_simple_$N --full --seed=100 --cv=3 --prior=simple
#python $faststruct/structure.py -K 5 --input=core_v0.7.pruneddata --output=testoutput_logistic --full --seed=100 --cv=3 --prior=logistic

#python $faststruct/distruct.py -K 5 --input=testoutput_simple --output=testoutput_simple_distruct.svg


end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"
