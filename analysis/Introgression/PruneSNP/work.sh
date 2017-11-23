echo "3000 rice list"
ln -s ~/Rice/Rice_population_sequence/Rice_3000/GigaScience/rice_line_ALL_3000.anno.list ./

echo "download 3k: Subsets 3k RG SNPs release 1.0, http://snp-seek.irri.org/_download.zul;jsessionid=807F4FF0CB9DE8B30181A140AC7EF93B"
#previous 3K_coreSNP-v2.1.* version is not avaliable anymore, so we use this release 1.0 version to update the result
#3024 strain in this release 1.0, we use the previous 3000 only
#404K CoreSNP dataset, called vs Nipponbare MSU7/IRGSP1.0 genome, PLINK bed file
#404K CoreSNP dataset, called vs Nipponbare MSU7/IRGSP1.0 genome, PLINK bim file
#404K CoreSNP dataset, called vs Nipponbare MSU7/IRGSP1.0 genome, PLINK fam file
#404K CoreSNP dataset README
wget https://s3.amazonaws.com/3kricegenome/snpseek-dl/3krg-base-filt-core-v0.7/readme_core_v0.7.txt
wget https://s3.amazonaws.com/3kricegenome/snpseek-dl/3krg-base-filt-core-v0.7/core_v0.7.bim.gz
wget https://s3.amazonaws.com/3kricegenome/snpseek-dl/3krg-base-filt-core-v0.7/core_v0.7.fam.gz
wget https://s3.amazonaws.com/3kricegenome/snpseek-dl/3krg-base-filt-core-v0.7/core_v0.7.bim.gz
gunzip -d core_v0.7.bed.gz 
gunzip -d core_v0.7.bim.gz 
gunzip -d core_v0.7.fam.gz 
#remove 24 individual that not in previous 3k genome
cp core_v0.7.structure.nosex core_v0.7.strain.list
python listdiff.py rice_line_ALL_3000.anno.list core_v0.7.strain.list | grep "list2" | cut -d" " -f4 | awk '{print $1"\t"$1}' > core_v0.7.strain.only.list

echo "404k SNPs, which mean one SNP per 900 bp. We use --indep-pairwise 200 5 0.1 to trim SNP into 16798, which is one SNP per 22kb"
sbatch plink_prune.sh
echo "convert plink files into structure"
sbatch plink_structure.sh

