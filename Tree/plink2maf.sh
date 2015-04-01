#/rhome/cjinfeng/software/tools/plink/plink_linux_x86_64_v1.09/plink --file 3K_coreSNP-v2.1 --recode vcf-iid --out 3K_coreSNP-v2.1 
#vcf-to-tab < 3K_coreSNP-v2.1.vcf > 3K_coreSNP-v2.1.tab
#perl vcf_tab_to_fasta_alignment.pl -i test.tab > test.fasta
perl vcf_tab_to_fasta_alignment.pl -i 3K_coreSNP-v2.1.tab > 3K_coreSNP-v2.1.fasta
