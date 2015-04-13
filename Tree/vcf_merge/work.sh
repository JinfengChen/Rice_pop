sed 's/Chr//' HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.vcf > HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1_12.vcf
/opt/vcftools/0.1.12b/bin/vcftools --vcf HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1_12.vcf --out HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1 --chr 1 --temp ./ --recode
/opt/vcftools/0.1.12b/bin/vcftools --vcf 3K_coreSNP-v2.1.binary.vcf --out 3K_coreSNP-v2.1.binary.1 --chr 1 --temp ./ --recode
/rhome/cjinfeng/software/tools/tabix/tabix-0.2.6/bgzip 3K_coreSNP-v2.1.binary.1.recode.vcf
/rhome/cjinfeng/software/tools/tabix/tabix-0.2.6/tabix -p vcf 3K_coreSNP-v2.1.binary.1.recode.vcf.gz
/rhome/cjinfeng/software/tools/tabix/tabix-0.2.6/bgzip HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.recode.vcf
/rhome/cjinfeng/software/tools/tabix/tabix-0.2.6/tabix -p vcf HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.recode.vcf.gz
/opt/vcftools/0.1.12b/bin/vcf-isec -f 3K_coreSNP-v2.1.binary.1.recode.vcf.gz HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.recode.vcf.gz > log 2> log2 &
/opt/vcftools/0.1.12b/bin/vcf-merge 3K_coreSNP-v2.1.binary.1.recode.vcf.gz HEG4_EG4_A119_A123_NB_SNPs.noRepeats.selectedSNPs.1.recode.vcf.gz > merge_chr1.vcf 2> log2 &

python Remove_Corrected_SNP.py > log 2> log2 &

