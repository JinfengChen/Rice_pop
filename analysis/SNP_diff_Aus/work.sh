echo "SNP difference among aus strains"
ln -s ../Zero_mPing_Strain/Ping_aus_strains.list ./
awk '{print $1"\t"$1}' Ping_aus_strains.list > Ping_aus_strains.list2
sbatch download_3k_SNP.sh
sbatch --array 1-3 gz_unzip_qsub.sh
sbatch --array 1-12 plink_vcf_chr_SNPdiff.sh
#SNPdiff
#Strains pairs\ttotal SNP\tboth diff from NB\tdiffered SNP\tstrain1 differed\tstrain2 differed
python merge_SNPdiff.py
cut -f4 NB_final_snp.aus_group.SNPdiff | perl ~/BigData/software/bin/numberStat.pl

