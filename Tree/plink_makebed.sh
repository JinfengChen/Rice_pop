#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=5gb
#PBS -l walltime=100:00:00
#PBS -V

cd $PBS_O_WORKDIR

prefix=3K_coreSNP-v2.1

if [ ! -e $prefix.binary.bed ]; then
echo "make-bed: convert to binary file"
/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --file $prefix --make-bed --out $prefix.binary
echo "make-bed: done"
fi

if [ ! -e $prefix.binary.vcf ]; then 

echo "extract vcf for individual chromosome"
for chr in {1..12};
do
/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --bfile $prefix.binary --recode vcf-iid --chr $chr --out $prefix.binary.$chr
done

echo "merge individual chromosome vcf into one"
python Merge_Chr_VCF.py --input $prefix.binary
rm $prefix.binary.temp.*

for chr in {1..12};
do
rm $prefix.binary.$chr.vcf $prefix.binary.$chr.log $prefix.binary.$chr.nosex
done

fi

if [ ! -e $prefix.binary.fasta ]; then

echo "convert vcf to tab and tab to fasta"
module load vcftools
vcf-to-tab < $prefix.binary.vcf > $prefix.binary.tab
perl vcf_tab_to_fasta_alignmentv1.pl -i $prefix.binary.tab > $prefix.binary.tab.pos

fi

echo "Done"

