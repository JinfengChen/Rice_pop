#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=30G
#SBATCH --time=10:00:00
#SBATCH --output=run_faststruct.sh.%A_%a.stdout
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

faststruct=/rhome/cjinfeng/BigData/software/population_genetics/fastStructure

python $faststruct/structure.py -K 5 --input=core_v0.7.pruneddata --output=testoutput_simple --full --seed=100 --prior=simple
python $faststruct/structure.py -K 5 --input=core_v0.7.pruneddata --output=testoutput_logistic --full --seed=100 --prior=logistic

#python $faststruct/distruct.py -K 5 --input=testoutput_simple --output=testoutput_simple_distruct.svg


end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"
