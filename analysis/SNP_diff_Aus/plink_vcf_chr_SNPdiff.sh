#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --time=40:00:00
#SBATCH --output=plink_vcf_chr_SNPdiff.sh.%A_%a.stdout
#SBATCH -p intel
#SBATCH --workdir=./

N=$SLURM_ARRAY_TASK_ID
if [ ! $N ]; then
    N=1
fi

prefix=NB_final_snp
plink=/rhome/cjinfeng/BigData/software/plink/plink_linux_x86_64_v1.90/plink

start=`date +%s`

#need *.bed, *.bim and *.fam files as binary input
echo "extract vcf for individual chromosome"
$plink --bfile $prefix --recode vcf-iid --keep Ping_aus_strains.list2 --chr $N --out $prefix.aus_group.$N

python SNP_differences.py --input $prefix.aus_group.$N\.vcf > $prefix.aus_group.vcf.$N.log

end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"
