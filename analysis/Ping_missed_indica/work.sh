echo "cp"
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470252_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470257_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470279_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470300_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470383_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470404_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470480_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470491_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470492_RelocaTEi/ ./
#cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/ERS470510_RelocaTEi/ ./

echo "rerun Ping"
#generate raw Ping call from each strain
python ReNameSRA_sum_Ping_raw.py --input Test_Ping
#merge raw Ping call from each strains into a GFF containing all Ping loci in the population
python RunRelocaTEi_CombinedGFF_raw.py --input Test_Ping
#genotype Ping in each strain using all known Ping loci
python ReNameSRA_sum_Ping.py --input Test_Ping --gff Test_Ping.CombinedGFF.ALL_raw.gff
#merge Ping call from each strains into a GFF containing all Ping loci in the population
python RunRelocaTEi_CombinedGFF.py --input Test_Ping

echo "Rerun Ping on 3k"
cp -R ../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping/*_RelocaTEi/ ./ &
#python ReNameSRA_sum_Ping_raw.py --input Rice3k_3000_RelocaTEi_Ping_Rerun
python ReNameSRA_sum_Ping_raw_qsub.py --input Rice3k_3000_RelocaTEi_Ping_Rerun
python RunRelocaTEi_CombinedGFF_raw.py --input Rice3k_3000_RelocaTEi_Ping_Rerun
python ReNameSRA_sum_Ping.py --input Rice3k_3000_RelocaTEi_Ping_Rerun --gff Rice3k_3000_RelocaTEi_Ping_Rerun.CombinedGFF.ALL_raw.gff
python RunRelocaTEi_CombinedGFF.py --input Rice3k_3000_RelocaTEi_Ping_Rerun

#Ping strain list
awk '$2>0' Rice3k_3000_RelocaTEi_Ping_Rerun.raw.summary | cut -f5| sed 's/IRIS/IRIS_/g' | grep -v "Name" > Rice3k_3000_RelocaTEi_Ping_Rerun.raw.summary.strains.list
python sum_pop_distri_general.py --input Rice3k_3000_RelocaTEi_Ping_Rerun.raw.summary.strains.list

