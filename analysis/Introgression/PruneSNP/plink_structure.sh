#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=100G
#SBATCH --time=40:00:00
#SBATCH --output=plink2structure.sh.%A_%a.stdout
#SBATCH -p intel
#SBATCH --workdir=./

#prefix=3K_coreSNP-v2.1
prefix=core_v0.7.pruneddata

#java -Xmx10g -Xms512M -jar ~/BigData/software/population_genetics/Structure/PGDSpider_2.1.1.3/PGDSpider2-cli.jar -inputfile 3K_coreSNP-v2.1.ped -inputformat ped -outputfile test.str.txt -outputformat STRUCTURE
plink=/rhome/cjinfeng/BigData/software/plink/plink_linux_x86_64_v1.09/plink

$plink --bfile $prefix --recode structure --out $prefix.structure



echo "Done"

