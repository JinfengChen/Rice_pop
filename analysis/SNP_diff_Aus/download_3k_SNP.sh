#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=10G
#SBATCH --time=40:00:00
#SBATCH --output=download_3K_SNP.sh.%A_%a.stdout
#SBATCH -p intel
#SBATCH --workdir=./

start=`date +%s`

#3K RG 29mio biallelic SNPs Dataset
wget https://s3.amazonaws.com/3kricegenome/reduced/NB_final_snp.bed.gz
wget https://s3.amazonaws.com/3kricegenome/reduced/NB_final_snp.bim.gz
wget https://s3.amazonaws.com/3kricegenome/reduced/NB_final_snp.fam.gz
wget https://s3.amazonaws.com/3kricegenome/reduced/README-3kRG-full-SNP-v1.txt

end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"

