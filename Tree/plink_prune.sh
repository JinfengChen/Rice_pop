#/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --file 3K_coreSNP-v2.1 --indep-pairwise 50 5 0.5
/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --file 3K_coreSNP-v2.1 --extract plink.prune.in --make-bed --out 3K_coreSNP-v2.1.pruneddata
#/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --file 3K_coreSNP-v2.1.pruneddata --recode vcf-iid --out 3K_coreSNP-v2.1.pruneddata 
