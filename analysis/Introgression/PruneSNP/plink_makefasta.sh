#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=100G
#SBATCH --time=40:00:00
#SBATCH --output=plink_makefasta.sh.%A_%a.stdout
#SBATCH -p intel
#SBATCH --workdir=./

#prefix=3K_coreSNP-v2.1
prefix=core_v0.7

#if [ ! -e $prefix.binary.bed ]; then
#echo "make-bed: convert to binary file"
#/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --file $prefix --make-bed --out $prefix.binary
#echo "make-bed: done"
#fi

plink=/rhome/cjinfeng/BigData/software/plink/plink_linux_x86_64_v1.09/plink

if [ ! -e $prefix.vcf ]; then 

echo "extract vcf for individual chromosome"
for chr in {1..12};
do
$plink --bfile $prefix --recode vcf-iid --chr $chr --out $prefix.$chr
done

echo "merge individual chromosome vcf into one"
python Merge_Chr_VCF.py --input $prefix
rm $prefix.temp.*

for chr in {1..12};
do
rm $prefix.$chr.vcf $prefix.$chr.log $prefix.$chr.nosex
done

fi

if [ ! -e $prefix.fasta ]; then

echo "convert vcf to tab and tab to fasta"
module load vcftools
vcf-to-tab < $prefix.vcf > $prefix.tab
perl vcf_tab_to_fasta_alignmentv1.pl -i $prefix.tab > $prefix.tab.pos

fi

echo "Done"

