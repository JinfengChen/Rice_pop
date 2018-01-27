#round1
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test
cd Ping_test
cat *.reads_1.fq > test_1.fq
cat *.reads_2.fq > test_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test.assembly 31 -shortPaired -fastq -separate test_1.fq test_2.fq 
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#rm *.assembly *.reads* -R

perl ~/BigData/software/bin/fastaDeal.pl --reverse --complement up_round1.fa > up_round1_rc.fa

#round2
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round1 > log 2>&1 &
cd Ping_test_Round1
#repeat round1
perl ~/BigData/software/bin/fastaDeal.pl --reverse --complement up_round2.fa > up_round2_rc.fa

#round3
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round2 > log 2>&1 &
cd Ping_test_Round2
#repeat round1
perl ~/BigData/software/bin/fastaDeal.pl --reverse --complement up_round2.fa > up_round2_rc.fa

