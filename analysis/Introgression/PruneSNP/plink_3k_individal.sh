#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=100G
#SBATCH --time=40:00:00
#SBATCH --output=plink_3k_individal.sh.%A_%a.stdout
#SBATCH -p intel
#SBATCH --workdir=./

#prefix=3K_coreSNP-v2.1
prefix=core_v0.7

plink=/rhome/cjinfeng/BigData/software/plink/plink_linux_x86_64_v1.09/plink

$plink --bfile $prefix --remove core_v0.7.strain.only.list


echo "Done"

