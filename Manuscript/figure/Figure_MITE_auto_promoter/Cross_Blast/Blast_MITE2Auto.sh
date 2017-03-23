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

STRAIN=(OGU_1 OID_1 ONI_1 ORU_1 OME_1)
#STRAIN=(MSU7 OID ONI ORU ORU_Australia ORU_W1943 OGL OBA OME OLO OGU OPU OBR)
#STRAIN=(DJ123 IR64 MSU7 OID ONI ORU ORU_Australia ORU_W1943)
#STRAIN=(OGL OBA OME OLO OGU OPU OBR)
#STRAIN=(DJ123 IR64)
for SAMPLE in ${STRAIN[@]};
do
   echo $SAMPLE
   #step1, run Target
   if true; then
       python Blast_MITE2Auto.py --input Target_Auto_$SAMPLE
   fi
done

end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"
