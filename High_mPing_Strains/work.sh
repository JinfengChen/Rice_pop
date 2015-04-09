echo "ID"
python ReNameSRA_subset.py --input high_mping_strain.id
cp high_mping_strain.id.download.list high_mping_strain.id.download.list.IRRI
cp high_mping_strain.id.download.list high_mping_strain.id.download.list.CAAS
cat high_mping_strain.id.download.list.CAAS high_mping_strain.id.download.list.IRRI > high_mping_strain.id.download.list

echo "download"
python ReNameSRA_down.py --output Japonica_fastq > log 2> log2 &
python ReNameSRA_merge.py --input Japonica_fastq > log 2> log2 &
rm Japonica_fastq/ERS4*/*.sra

echo "Mapping"
ls `pwd`/Japonica_fastq/ERS4*/*_1.fastq.gz | sed 's/_1.fastq.gz/_?.fastq.gz/' | awk '{print $1"\t"500"\t"500"\t100.00"}' > Japonica_fastq.list
perl list2csv.pl --list Japonica_fastq.list
perl runMapping.pl --ref /rhome/cjinfeng/HEG4_cjinfeng/MappingReads/input/MSU_r7.fa --lib in_libs.HEG4.csv --group in_groups.HEG4.csv --project High_mPing
bash High_mPing.sh > log 2> log2 &

echo "Mapping to HEG4 Chr01"
perl runMapping.pl --ref /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/High_mPing_Strains/reference/HEG4.Chr01.fa --lib in_libs.HEG4.csv --group in_groups.HEG4.csv --project High_mPing_Chr01

echo "Mapping to special ping locus"
perl runMapping.pl --ref /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/High_mPing_Strains/reference/Ping_S_flanking_1000.fa --lib in_libs.HEG4.csv --group in_groups.HEG4.csv --project Ping_S
perl runMapping.pl --ref /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/High_mPing_Strains/reference/Ping_S_flanking_1000.fa --lib in_libs.HEG4_RAW.csv --group in_groups.HEG4_RAW.csv --project Ping_S_HEG4


echo "RelocaTEi"
python ReNameSRA_RelocaTEi.py --input Japonica_fastq --output Japonica_fastq_RelocaTEi_Pong --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/pong.fa > log 2> log2 &
python ReNameSRA_RelocaTEi.py --input Japonica_fastq --output Japonica_fastq_RelocaTEi_Ping --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa > log 2> log2 &

echo "find Ping and Pong using internal difference"
python PickPing.py --input Japonica_fastq_RelocaTEi_Pong/ERS470370_RelocaTEi | less -S


echo "Mapping to new Ping and Pong loci"
perl runMapping.pl --ref /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/High_mPing_Strains/reference/new_ping_pong_flanking_1000.fa --lib in_libs.HEG4.csv --group in_groups.HEG4.csv --project New_Ping_Pong

