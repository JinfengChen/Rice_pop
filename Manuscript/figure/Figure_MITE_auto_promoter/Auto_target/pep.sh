#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem=100G
#SBATCH --time=40:00:00
#SBATCH --output=slurm.stdout
#SBATCH -p intel
#SBATCH --workdir=./

#sbatch --array 1 run_speedseq_qsub.sh

PATH=~/BigData/software/bedtools2-2.19.0/bin/:$PATH
module load cd-hit/4.6.4
#module load bedtools/2.25.0
module load mafft
module load treebest
module load fasttree/2.1.8
module load ncbi-blast/2.2.26

start=`date +%s`

CPU=$SLURM_NTASKS
if [ ! $CPU ]; then
   CPU=2
fi

N=$SLURM_ARRAY_TASK_ID
if [ ! $N ]; then
    N=$1
fi

echo "CPU: $CPU"
echo "N: $N"

STRAIN=(MSU7 OID ONI ORU ORU_Australia ORU_W1943 OGL OBA OME OLO OGU OPU OBR)
#STRAIN=(DJ123 IR64 MSU7 OID ONI ORU ORU_Australia ORU_W1943)
#STRAIN=(OGL OBA OME OLO OGU OPU OBR)
#STRAIN=(DJ123 IR64)
for SAMPLE in ${STRAIN[@]};
do
   echo $SAMPLE
   #step1, run Target
   if true; then
       rm -Rf ./query
       mkdir ./query
       cp ./Tpase/angiosperm_* ./query/
       mkdir Target_Auto_$SAMPLE
       formatdb -i ./reference/$SAMPLE\.fa -p F -o T -n ./reference/$SAMPLE\.fa -s T
       perl /rhome/cjinfeng/BigData/software/Target/brad/TARGeT/reads_indexer.pl -i ./reference/$SAMPLE\.fa
       python scripts/make_target_peps_general.py `pwd`/query `pwd`/Target_Auto_$SAMPLE `pwd`/reference/$SAMPLE\.fa Target_Run_$SAMPLE
       sbatch Target_Run_$SAMPLE\_angiosperm_hAT_tpase.sh 
       sbatch Target_Run_$SAMPLE\_angiosperm_mutator_tpase.sh 
       sbatch Target_Run_$SAMPLE\_angiosperm_mariner_tpase.sh 
       sbatch Target_Run_$SAMPLE\_angiosperm_harbinger_tpase.sh
   fi
   #step2, run activeTE
   if false; then
       for target_dir in $(ls -d Target_Auto_$SAMPLE/Target_Run_$SAMPLE\_angiosperm_*);
       do
           echo $target_dir
           python Target_Pep_Pipe.py --input $target_dir --reference ./reference/$SAMPLE\.fa
           cp mafft_qsub.sh $target_dir\_activeTE/nonredundant_pep_union-10kb_c80_multi/ 
       done
   fi
done

##not using anymore
#python scripts/make_target_peps_general.py `pwd`/query `pwd`/Target_Mariner `pwd`/reference/MSU7.fa Target_Run_Mariner_MSU7
#sbatch Target_Run_Mariner_MSU7_angiosperm_mariner_tpase.sh
#python Target_Pep_Pipe.py --input Target_Mariner/Target_Run_Mariner_MSU7_angiosperm_mariner_tpase_angiosperm_mariner_tpase_2017_03_16_124024

#python scripts/make_target_peps_general.py `pwd`/query `pwd`/Target_Mutator `pwd`/reference/MSU7.fa Target_Run_Mutator_MSU7
#sbatch Target_Run_Mutator_MSU7_angiosperm_mutator_tpase.sh
#python Target_Pep_Pipe.py --input Target_Mutator/Target_Run_Mutator_MSU7_angiosperm_mutator_tpase_angiosperm_mutator_tpase_2017_03_16_142926 --cpu $CPU

#python scripts/make_target_peps_general.py `pwd`/query `pwd`/Target_hAT `pwd`/reference/MSU7.fa Target_Run_hAT_MSU7
#sbatch Target_Run_hAT_MSU7_angiosperm_hAT_tpase.sh
#python Target_Pep_Pipe.py --input Target_hAT/Target_Run_hAT_MSU7_angiosperm_hAT_tpase_angiosperm_hAT_tpase_2017_03_16_143822 --cpu $CPU

end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"
