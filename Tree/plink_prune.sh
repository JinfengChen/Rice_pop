#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=5gb
#PBS -l walltime=100:00:00
#PBS -V

cd $PBS_O_WORKDIR

prefix=3K_coreSNP-v2.1

/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --file $prefix --indep-pairwise 50 5 0.5
/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --file $prefix --extract plink.prune.in --make-bed --out $prefix.pruneddata
/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --bfile $prefix.pruneddata --recode vcf-iid --out $prefix.pruneddata
module load vcftools
vcf-to-tab < $prefix.pruneddata.vcf > $prefix.pruneddata.tab
perl vcf_tab_to_fasta_alignmentv1.pl -i $prefix.pruneddata.tab > $prefix.pruneddata.tab.pos

echo "Done"
