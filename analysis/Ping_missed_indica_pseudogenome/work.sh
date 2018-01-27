echo "test 10 strains"
python ReNameSRA_subset.py --input Ping_test.list
python ReNameSRA_down.py --output Ping_test > log 2>&1
python ReNameSRA_merge.py --input Ping_test > log 2>&1 &
python Run_Merge_multi_sample.py --fastq_dir Ping_test/ > log 2>&1 &

echo "all RelocaTE2 depth Ping strains"
ln -s ../Zero_mPing_Strain/RelocaTE2_Depth_Ping.txt ./
head -n 220 RelocaTE2_Depth_Ping.txt > RelocaTE2_Depth_Ping1.txt
head -n 242 RelocaTE2_Depth_Ping.txt > RelocaTE2_Depth_Ping2.txt

python ReNameSRA_subset.py --input RelocaTE2_Depth_Ping1.txt
python ReNameSRA_down.py --output Ping_Depth > log 2>&1
python ReNameSRA_merge.py --input Ping_Depth > log 2>&1 &
python Run_Merge_multi_sample.py --fastq_dir Ping_Depth/ > log 2>&1 &

python ReNameSRA_subset.py --input RelocaTE2_Depth_Ping2.txt
python ReNameSRA_down.py --output Ping_Depth > log 2>&1
python ReNameSRA_merge.py --input Ping_Depth > log 2>&1 &
python Run_Merge_multi_sample.py --fastq_dir Ping_Depth/ > log 2>&1 &

echo "Ping Psuedo"
#down stream, Chr2    29244757
perl ~/BigData/software/bin/fastaDeal.pl --get_id Chr2 ~/BigData/00.RD/seqlib/MSU_r7.fa > MSU7_Chr2.fa
perl ~/BigData/software/bin/fastaDeal.pl -sub 29244757-29246757 MSU7_Chr2.fa > MSU7_Chr2_down.fa
cat up.fa ping.fa MSU7_Chr2_down.fa > Ping_test_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_test_Pseudo.fa > Ping_test_Pseudo_RF.fa
#down stream new, ERS470257, ERR627076.1574849(71M12S)/ERR623076.1002340(37M46S)
#ERS470257, ERR623599.1015627(58M25S) is consistent with 470257
#TAATAATGGGCGGCTGACCGCGTGTGGGTGCGGGCGCACGGTCGCCTCCCCGCCC
#new Ping Psuedo
cat up.fa ping.fa down.fa > Ping_New_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_New_Pseudo.fa > Ping_New_Pseudo_RF.fa
#supported by paired end from both end and flanking
#ERS470252, ERR623005.970209 and ERR623005.750760

#round1 local assembly
cat up_round1_rc.fa ping.fa down.fa > Ping_Round1_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round1_Pseudo.fa > Ping_Round1_Pseudo_RF.fa

#round2 local assembly
cat up_round2_rc.fa ping.fa down.fa > Ping_Round2_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round2_Pseudo.fa > Ping_Round2_Pseudo_RF.fa

#round3 local assembly
cat up_round3.fa ping.fa down.fa > Ping_Round3_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo.fa > Ping_Round3_Pseudo_RF.fa

echo "Map reads to Ping Psuedo"
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_test_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test --genome Ping_test_Pseudo.fa > log 2>&1 &
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_New_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test --genome Ping_New_Pseudo.fa > log 2>&1 &
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round1_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round1 --genome Ping_Round1_Pseudo.fa > log 2>&1 &
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round2_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round2 --genome Ping_Round2_Pseudo.fa > log 2>&1 &
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round3 --genome Ping_Round3_Pseudo.fa > log 2>&1 &


echo "check up and down sequence"
cat up.fa down.fa > up_down.fa
cat up_round2_rc.fa down.fa > up_down.fa
blastall -p blastn -i up_down.fa -d ~/BigData/00.RD/seqlib/MSU_r7.fa
blastall -p blastn -i up_down.fa -d ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/Indica/OID.fa
blastall -p blastn -i up_down.fa -d ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/Indica_R498/R498_Chr.fasta

