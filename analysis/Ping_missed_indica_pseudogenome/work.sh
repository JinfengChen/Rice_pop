echo "Ping_1479_recall"
echo "test 10 strains"
python ReNameSRA_subset.py --input Ping_test.list
python ReNameSRA_down.py --output Ping_test > log 2>&1
python ReNameSRA_merge.py --input Ping_test > log 2>&1 &
python Run_Merge_multi_sample.py --fastq_dir Ping_test/ > log 2>&1 &

echo "all RelocaTE2 depth Ping strains"
ln -s ../Zero_mPing_Strain/RelocaTE2_Depth_Ping.txt ./
head -n 242 RelocaTE2_Depth_Ping.txt > RelocaTE2_Depth_Ping1.txt
tail -n 220 RelocaTE2_Depth_Ping.txt > RelocaTE2_Depth_Ping2.txt

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

#round4 local assembly
cat up_round3.fa ping.fa down_round1_rc.fa > Ping_Round4_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round4_Pseudo.fa > Ping_Round4_Pseudo_RF.fa

#round5 local assembly
cat up_round4.fa ping.fa down_round2_rc.fa > Ping_Round5_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round5_Pseudo.fa > Ping_Round5_Pseudo_RF.fa

#round6 local assembly
cat up_round4.fa ping_trunc.fa down_round2_rc.fa > Ping_Round6_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round6_Pseudo.fa > Ping_Round6_Pseudo_RF.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round6_Pseudo_noPing.fa > Ping_Round6_Pseudo_noPing_RF.fa

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
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round4_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round4 --genome Ping_Round4_Pseudo.fa > log 2>&1 &
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round5_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round5 --genome Ping_Round5_Pseudo.fa > log 2>&1 &
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round6_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round6 --genome Ping_Round6_Pseudo.fa > log 2>&1 &

echo "check up and down sequence"
cat up.fa down.fa > up_down.fa
cat up_round2_rc.fa down.fa > up_down.fa
blastall -p blastn -i up_down.fa -d ~/BigData/00.RD/seqlib/MSU_r7.fa
blastall -p blastn -i up_down.fa -d ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/Indica/OID.fa
blastall -p blastn -i up_down.fa -d ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/Indica_R498/R498_Chr.fasta

echo "Mapped all Ping strains to Psuedo genome with/without Ping"
mkdir Ping_Depth_Psuedo_noPing_bam
cd Ping_Depth_Psuedo_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_Ping_bam --genome Ping_Round6_Pseudo.fa > log 2>&1 &

mkdir Ping_Depth_Psuedo_noPing_bam
cd Ping_Depth_Psuedo_noPing_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_noPing_bam --genome Ping_Round6_Pseudo_noPing.fa > log 2>&1 &

echo "Ping 1491 bp status, Ping_up:1495-2986, Ping_up:1495-1497"
python mPing_Boundary_Coverage_Ping_1491bp.py --bam_ref Ping_Depth_Psuedo_noPing_bam --bam_pseudo Ping_Depth_Psuedo_Ping_bam > Ping_1491bp_status.txt
awk '$5~/covered/ && $6~/covered/' Ping_1491bp_status.10bp_flank.txt | wc -l
awk '$5!~/covered/ && $6~/covered/' Ping_1491bp_status.10bp_flank.txt | wc -l
awk '$5~/covered/ && $6!~/covered/' Ping_1491bp_status.10bp_flank.txt | wc -l

#test
awk '$5~/covered/ && $6~/covered/' Ping_1491bp_status.txt > Ping_1491bp_status.txt.insertion.list
awk '$5!~/covered/ && $6~/covered/' Ping_1491bp_status.txt > Ping_1491bp_status.txt.No_1.list
awk '$5~/covered/ && $6!~/covered/' Ping_1491bp_status.txt > Ping_1491bp_status.txt.No_2.list
awk '$5!~/covered/ && $6!~/covered/' Ping_1491bp_status.txt > Ping_1491bp_status.txt.No_3.list

#
cat Ping_1491bp_status.txt.insertion.list Ping_1491bp_status.txt.No_1.list Ping_1491bp_status.txt.No_2.list > Ping_1491bp_status.insertion_No1_2.txt
cut -f2 Ping_1491bp_status.insertion_No1_2.txt > Ping_1491bp_status.insertion_No1_2.acc.txt
#3 of 108 is not new
python ~/BigData/software/bin/listdiff.py Ping_1491bp_status.insertion_No1_2.acc.txt ../../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt | less -S
awk '{print $1"\tChr13\t1479\t1482\t+"}' Ping_1491bp_status.insertion_No1_2.txt > Ping_1491bp_status.insertion_No1_2.PreGFF.list


echo "who else missed"
#213 missed by RelocaTE2
python ~/BigData/software/bin/listdiff.py ../Zero_mPing_Strain/RelocaTE2_Depth_Ping.txt ../Ping_missed_indica/Rice3k_3000_RelocaTEi_Ping_Rerun.raw.summary.strains.list| grep "list1" | cut -d" " -f4 > ../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt
#108 is 1491bp Ping
cat Ping_1491bp_status.txt.insertion.list Ping_1491bp_status.txt.No_1.list Ping_1491bp_status.txt.No_2.list | cut -f2 | sort | uniq > Ping_1491bp_status.insertion_No1_2.txt
#108 is still missing
python ~/BigData/software/bin/listdiff.py Ping_1491bp_status.insertion_No1_2.txt ../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt | grep "list2" | cut -d" " -f4 > Ping_1491bp_status.still_missing.txt
python sum_pop_distri_general.py --input Ping_1491bp_status.still_missing.txt

echo "echo Ping_3230_recall"
mkdir Ping_3230_recall
mkdir Ping_3230_recall/Ping_test
awk '$2>3201 && $2<3230' ../Zero_mPing_Strain/ping_3k_NM2.txt | cut -f1 > Ping_test.3230.list
python ReNameSRA_subset.py --input Ping_test.3230.list
cut -f2,5 Ping_test.3230.list.download.list | uniq | sort | uniq | sed 's/IRIS/IRIS_/' > Ping_test.3230.list.acc.txt
cut -f2 Ping_test.3230.list.acc.txt | awk '{print "cp Ping_1479_recall/Ping_Depth_Psuedo_Ping_bam/"$1"_Pseudo.NM2.bam* ./Ping_3230_recall/Ping_test/"}' > Ping_test.3230.cp.sh
cp Ping_1479_recall/Ping_Round6_Pseudo_RF.fa Ping_3230_recall/Ping_test/    
#get first few bp of flanking sequence using junction reads from bam files

#test fastq
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468298*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468186*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468595*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468605*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468412*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469412*.fastq.gz .
#make pseudogenome
#Round0
cat up_round0.fa ping_trun.fa down_round0.fa > Ping_Round0_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round0_Pseudo.fa > Ping_Round0_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round0_Pseudo.fa
mkdir Ping_test_Round0
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_3230_recall/Ping_test/*.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round0 --genome Ping_Round0_Pseudo.fa > log 2>&1 &
#assemble
mkdir Ping_test_local_assembly
cd Ping_test_local_assembly
cp ../../Ping_1479_recall/Ping_test_local_assembly/Get_List_Raw_Fastq* ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_3230_recall/Ping_test_Round0/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round0 > log 2>&1 &
cd Ping_test_Round0
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#rm *.assembly *.reads* -R
#Round1
cat up_round1.fa ping_trun.fa down_round1.fa > Ping_Round1_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round1_Pseudo.fa > Ping_Round1_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round1_Pseudo.fa
mkdir Ping_test_Round1
cd Ping_test_Round1
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_3230_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round1 --genome Ping_Round1_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_3230_recall/Ping_test_Round1/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round1 > log 2>&1 &
cd Ping_test_Round1
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#Round2
cat up_round2.fa ping_trun.fa down_round2.fa > Ping_Round2_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round2_Pseudo.fa > Ping_Round2_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round2_Pseudo.fa
mkdir Ping_test_Round2
cd Ping_test_Round2
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_3230_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round2 --genome Ping_Round2_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_3230_recall/Ping_test_Round2/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round2 > log 2>&1 &
cd Ping_test_Round2
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#Round3, just for building pseudogenome
cat up_round3.fa ping_trun.fa down_round3.fa > Ping_Round3_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo.fa > Ping_Round3_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo.fa
cat up_round3.fa down_round3.fa > Ping_Round3_Pseudo_noPing.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo_noPing.fa > Ping_Round3_Pseudo_noPing_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo_noPing.fa
#map to pseudo with ping
mkdir Ping_Depth_Psuedo_Ping_bam
cd Ping_Depth_Psuedo_Ping_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_Ping_bam --genome Ping_Round3_Pseudo.fa > log 2>&1 &
#map to pseduo without ping
mkdir Ping_Depth_Psuedo_noPing_bam
cd Ping_Depth_Psuedo_noPing_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_noPing_bam --genome Ping_Round3_Pseudo_noPing.fa > log 2>&1 &
echo "Ping 3230 bp status, Ping_up:516-3747, Ping_up:516-517"
python mPing_Boundary_Coverage_Ping_3230bp.py --bam_ref Ping_Depth_Psuedo_noPing_bam --bam_pseudo Ping_Depth_Psuedo_Ping_bam > Ping_3230bp_status.txt
awk '$5~/covered/ && $6~/covered/' Ping_3230bp_status.txt > Ping_3230bp_status.txt.insertion.list
awk '$5!~/covered/ && $6~/covered/' Ping_3230bp_status.txt > Ping_3230bp_status.txt.No_1.list
awk '$5~/covered/ && $6!~/covered/' Ping_3230bp_status.txt > Ping_3230bp_status.txt.No_2.list
awk '$5!~/covered/ && $6!~/covered/' Ping_3230bp_status.txt > Ping_3230bp_status.txt.No_3.list
#final list of strain having Ping 3230
cat Ping_3230bp_status.txt.insertion.list Ping_3230bp_status.txt.No_1.list Ping_3230bp_status.txt.No_2.list > Ping_3230bp_status.insertion_No1_2.txt

#1 of 21 is not new
cut -f2 Ping_3230bp_status.insertion_No1_2.txt > Ping_3230bp_status.insertion_No1_2.acc.txt
python ~/BigData/software/bin/listdiff.py Ping_3230bp_status.insertion_No1_2.acc.txt ../../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt | less -S
awk '{print $1"\tChr13\t3230\t3230\t+"}' Ping_3230bp_status.insertion_No1_2.txt > Ping_3230bp_status.insertion_No1_2.PreGFF.list


echo "echo Ping_1646_recall"
mkdir Ping_1645_recall
mkdir Ping_1645_recall/Ping_test_Round_Pre
awk '$2>1625 && $2<1646' ../Zero_mPing_Strain/ping_3k_NM2.txt | cut -f1 > Ping_test.1645.list
python ReNameSRA_subset.py --input Ping_test.1645.list 
cut -f2,5 Ping_test.1645.list.download.list | uniq | sort | uniq | sed 's/IRIS/IRIS_/' > Ping_test.1645.list.acc.txt
cut -f2 Ping_test.1645.list.acc.txt | awk '{print "cp Ping_1479_recall/Ping_Depth_Psuedo_Ping_bam/"$1"_Pseudo.NM2.bam* ./Ping_1645_recall/Ping_test_Round_Pre/"}' > Ping_test.1645.cp.sh
cp Ping_1479_recall/Ping_Round6_Pseudo_RF.fa Ping_1645_recall/Ping_test_Round_Pre/
bash Ping_test.1645.cp.sh
#
mkdir Ping_test
cd Ping_test
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469524*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469675*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469687*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469836*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470152*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468687*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469156*.fastq.gz ./
#Round0
mkdir Ping_test_Round0
cd Ping_test_Round0
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1645_recall/Ping_test/*.gz ./
cd ..
cat up_round0.fa ping_trun.fa down_round0.fa > Ping_Round0_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round0_Pseudo.fa > Ping_Round0_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round0_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round0 --genome Ping_Round0_Pseudo.fa > log 2>&1 &
#assemble
mkdir Ping_test_local_assembly
cd Ping_test_local_assembly
cp ../../Ping_1479_recall/Ping_test_local_assembly/Get_List_Raw_Fastq* ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1645_recall/Ping_test_Round0/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round0 > log 2>&1 &
cd Ping_test_Round0
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#rm *.assembly *.reads* -R
#Round0: up 10-30, down 1680-1690
#Round1
cat up_round1.fa ping_trun.fa down_round1.fa > Ping_Round1_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round1_Pseudo.fa > Ping_Round1_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round1_Pseudo.fa
mkdir Ping_test_Round1
cd Ping_test_Round1
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1645_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round1 --genome Ping_Round1_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1645_recall/Ping_test_Round1/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round1 > log 2>&1 &
cd Ping_test_Round1
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#Round2
cat up_round2.fa ping_trun.fa down_round2.fa > Ping_Round2_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round2_Pseudo.fa > Ping_Round2_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round2_Pseudo.fa
mkdir Ping_test_Round2
cd Ping_test_Round2
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1645_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round2 --genome Ping_Round2_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1645_recall/Ping_test_Round2/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round2 > log 2>&1 &
cd Ping_test_Round2
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#Round3, just for building pseudogenome
cat up_round3.fa ping_trun.fa down_round3.fa > Ping_Round3_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo.fa > Ping_Round3_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo.fa
cat up_round3.fa down_round3.fa > Ping_Round3_Pseudo_noPing.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo_noPing.fa > Ping_Round3_Pseudo_noPing_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo_noPing.fa
#map to pseudo with ping
mkdir Ping_Depth_Psuedo_Ping_bam
cd Ping_Depth_Psuedo_Ping_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_Ping_bam --genome Ping_Round3_Pseudo.fa > log 2>&1 &
#map to pseduo without ping
mkdir Ping_Depth_Psuedo_noPing_bam
cd Ping_Depth_Psuedo_noPing_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_noPing_bam --genome Ping_Round3_Pseudo_noPing.fa > log 2>&1 &
echo "Ping 1645 bp status, Ping_up:928-2555, Ping_up:928-929"
python mPing_Boundary_Coverage_Ping_1645bp.py --bam_ref Ping_Depth_Psuedo_noPing_bam --bam_pseudo Ping_Depth_Psuedo_Ping_bam > Ping_1645bp_status.txt
awk '$5~/covered/ && $6~/covered/' Ping_1645bp_status.txt > Ping_1645bp_status.txt.insertion.list
awk '$5!~/covered/ && $6~/covered/' Ping_1645bp_status.txt > Ping_1645bp_status.txt.No_1.list
awk '$5~/covered/ && $6!~/covered/' Ping_1645bp_status.txt > Ping_1645bp_status.txt.No_2.list
awk '$5!~/covered/ && $6!~/covered/' Ping_1645bp_status.txt > Ping_1645bp_status.txt.No_3.list
#final list of strain having Ping 1645
cat Ping_1645bp_status.txt.insertion.list Ping_1645bp_status.txt.No_1.list Ping_1645bp_status.txt.No_2.list > Ping_1645bp_status.insertion_No1_2.txt
#all 12 are found 
cut -f2 Ping_1645bp_status.insertion_No1_2.txt > Ping_1645bp_status.insertion_No1_2.acc.txt
python ~/BigData/software/bin/listdiff.py Ping_1645bp_status.insertion_No1_2.acc.txt ../../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt | less -S


echo "echo Ping_1321_recall"
awk '$2>1310 && $2<1321' ../Zero_mPing_Strain/ping_3k_NM2.txt | cut -f1 > Ping_test.1321.list
mkdir Ping_1321_recall
mkdir Ping_1321_recall/Ping_test_Round_Pre
python ReNameSRA_subset.py --input Ping_test.1321.list 
cut -f2,5 Ping_test.1321.list.download.list | uniq | sort | uniq | sed 's/IRIS/IRIS_/' > Ping_test.1321.list.acc.txt
cut -f2 Ping_test.1321.list.acc.txt | awk '{print "cp Ping_1479_recall/Ping_Depth_Psuedo_Ping_bam/"$1"_Pseudo.NM2.bam* ./Ping_1321_recall/Ping_test_Round_Pre/"}' > Ping_test.1321.cp.sh
cp Ping_1479_recall/Ping_Round6_Pseudo_RF.fa Ping_1321_recall/Ping_test_Round_Pre/
bash Ping_test.1321.cp.sh
#
mkdir Ping_test
cd Ping_test
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470325*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468163*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS467924*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468306*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468204*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS467926*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469707*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468005*.fastq.gz ./
cd ..
#Round0
mkdir Ping_test_Round0
cd Ping_test_Round0
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1321_recall/Ping_test/*.gz ./
cd ..
cat up_round0.fa ping_trun.fa down_round0.fa > Ping_Round0_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round0_Pseudo.fa > Ping_Round0_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round0_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round0 --genome Ping_Round0_Pseudo.fa > log 2>&1 &
#assemble
mkdir Ping_test_local_assembly
cd Ping_test_local_assembly
cp ../../Ping_1479_recall/Ping_test_local_assembly/Get_List_Raw_Fastq* ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1321_recall/Ping_test_Round0/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round0 > log 2>&1 &
cd Ping_test_Round0
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#rm *.assembly *.reads* -R
#Round1
cat up_round1.fa ping_trun.fa down_round1.fa > Ping_Round1_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round1_Pseudo.fa > Ping_Round1_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round1_Pseudo.fa
mkdir Ping_test_Round1
cd Ping_test_Round1
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1321_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round1 --genome Ping_Round1_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1321_recall/Ping_test_Round1/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round1 > log 2>&1 &
cd Ping_test_Round1
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#Round2
cat up_round2.fa ping_trun.fa down_round2.fa > Ping_Round2_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round2_Pseudo.fa > Ping_Round2_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round2_Pseudo.fa
mkdir Ping_test_Round2
cd Ping_test_Round2
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1321_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round2 --genome Ping_Round2_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1321_recall/Ping_test_Round2/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round2 > log 2>&1 &
cd Ping_test_Round2
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#Round3, just for building pseudogenome
cat up_round3.fa ping_trun.fa down_round3.fa > Ping_Round3_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo.fa > Ping_Round3_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo.fa
cat up_round3.fa down_round3.fa > Ping_Round3_Pseudo_noPing.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo_noPing.fa > Ping_Round3_Pseudo_noPing_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo_noPing.fa
#map to pseudo with ping
mkdir Ping_Depth_Psuedo_Ping_bam
cd Ping_Depth_Psuedo_Ping_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_Ping_bam --genome Ping_Round3_Pseudo.fa > log 2>&1 &
#map to pseduo without ping
mkdir Ping_Depth_Psuedo_noPing_bam
cd Ping_Depth_Psuedo_noPing_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_noPing_bam --genome Ping_Round3_Pseudo_noPing.fa > log 2>&1 &
echo "Ping 1321 bp status, Ping_up:1322-2640, Ping_up:1322-1323"
python mPing_Boundary_Coverage_Ping_1321bp.py --bam_ref Ping_Depth_Psuedo_noPing_bam --bam_pseudo Ping_Depth_Psuedo_Ping_bam > Ping_1321bp_status.txt
awk '$5~/covered/ && $6~/covered/' Ping_1321bp_status.txt > Ping_1321bp_status.txt.insertion.list
awk '$5!~/covered/ && $6~/covered/' Ping_1321bp_status.txt > Ping_1321bp_status.txt.No_1.list
awk '$5~/covered/ && $6!~/covered/' Ping_1321bp_status.txt > Ping_1321bp_status.txt.No_2.list
awk '$5!~/covered/ && $6!~/covered/' Ping_1321bp_status.txt > Ping_1321bp_status.txt.No_3.list
#final list of strain having Ping 1321
cat Ping_1321bp_status.txt.insertion.list Ping_1321bp_status.txt.No_1.list Ping_1321bp_status.txt.No_2.list > Ping_1321bp_status.insertion_No1_2.txt
cut -f2 Ping_1321bp_status.insertion_No1_2.txt > Ping_1321bp_status.insertion_No1_2.acc.txt
#2 of 12 not new
python ~/BigData/software/bin/listdiff.py Ping_1321bp_status.insertion_No1_2.acc.txt ../../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt
awk '{print $1"\tChr13\t1321\t1324\t+"}' Ping_1321bp_status.insertion_No1_2.txt > Ping_1321bp_status.insertion_No1_2.PreGFF.list


echo "echo Ping_1200_recall"
awk '$2>1150 && $2<1200' ../Zero_mPing_Strain/ping_3k_NM2.txt | cut -f1 > Ping_test.1200.list
mkdir Ping_1200_recall
mkdir Ping_1200_recall/Ping_test_Round_Pre
python ReNameSRA_subset.py --input Ping_test.1200.list 
cut -f2,5 Ping_test.1200.list.download.list | uniq | sort | uniq | sed 's/IRIS/IRIS_/' > Ping_test.1200.list.acc.txt
cut -f2 Ping_test.1200.list.acc.txt | awk '{print "cp Ping_1479_recall/Ping_Depth_Psuedo_Ping_bam/"$1"_Pseudo.NM2.bam* ./Ping_1200_recall/Ping_test_Round_Pre/"}' > Ping_test.1200.cp.sh
cp Ping_1479_recall/Ping_Round6_Pseudo_RF.fa Ping_1200_recall/Ping_test_Round_Pre/
bash Ping_test.1200.cp.sh
#
mkdir Ping_test
cd Ping_test
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470302*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470303*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470308*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470412*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470493*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469112*.fastq.gz .
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468063*.fastq.gz .
cd ..
#Round0
mkdir Ping_test_Round0
cd Ping_test_Round0
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1200_recall/Ping_test/*.gz ./
cd ..
cat up_round0.fa ping_trun.fa down_round0.fa > Ping_Round0_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round0_Pseudo.fa > Ping_Round0_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round0_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round0 --genome Ping_Round0_Pseudo.fa > log 2>&1 &
#assemble
mkdir Ping_test_local_assembly
cd Ping_test_local_assembly
cp ../../Ping_1479_recall/Ping_test_local_assembly/Get_List_Raw_Fastq* ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1200_recall/Ping_test_Round0/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round0 > log 2>&1 &
cd Ping_test_Round0
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#rm *.assembly *.reads* -R
#Round1
#Round1
cat up_round1.fa ping_trun.fa down_round1.fa > Ping_Round1_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round1_Pseudo.fa > Ping_Round1_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round1_Pseudo.fa
mkdir Ping_test_Round1
cd Ping_test_Round1
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1200_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round1 --genome Ping_Round1_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1200_recall/Ping_test_Round1/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round1 > log 2>&1 &
cd Ping_test_Round1
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#Round2
cat up_round2.fa ping_trun.fa down_round2.fa > Ping_Round2_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round2_Pseudo.fa > Ping_Round2_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round2_Pseudo.fa
mkdir Ping_test_Round2
cd Ping_test_Round2
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1200_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round2 --genome Ping_Round2_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_1200_recall/Ping_test_Round2/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round2 > log 2>&1 &
cd Ping_test_Round2
cat *.upreads_1.fq > test_upreads_1.fq
cat *.upreads_2.fq > test_upreads_2.fq
cat *.downreads_1.fq > test_downreads_1.fq
cat *.downreads_2.fq > test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_upreads.assembly 31 -shortPaired -fastq -separate test_upreads_1.fq test_upreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_upreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
/rhome/cjinfeng/BigData/software/Velvet/velvet/velveth test_downreads.assembly 31 -shortPaired -fastq -separate test_downreads_1.fq test_downreads_2.fq
/rhome/cjinfeng/BigData/software/Velvet/velvet/velvetg test_downreads.assembly -ins_length 400 -exp_cov 50 -min_contig_lgth 200 -scaffolding yes
#Round3, just for building pseudogenome
cat up_round3.fa ping_trun.fa down_round3.fa > Ping_Round3_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo.fa > Ping_Round3_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo.fa
cat up_round3.fa down_round3.fa > Ping_Round3_Pseudo_noPing.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo_noPing.fa > Ping_Round3_Pseudo_noPing_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo_noPing.fa
#map to pseudo with ping
mkdir Ping_Depth_Psuedo_Ping_bam
cd Ping_Depth_Psuedo_Ping_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_Ping_bam --genome Ping_Round3_Pseudo.fa > log 2>&1 &
#map to pseduo without ping
mkdir Ping_Depth_Psuedo_noPing_bam
cd Ping_Depth_Psuedo_noPing_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_noPing_bam --genome Ping_Round3_Pseudo_noPing.fa > log 2>&1 &
echo "Ping 1200 bp status, Ping_up:1295-2263, Ping_up:1295-1296"
python mPing_Boundary_Coverage_Ping_1200bp.py --bam_ref Ping_Depth_Psuedo_noPing_bam --bam_pseudo Ping_Depth_Psuedo_Ping_bam > Ping_1200bp_status.txt
awk '$5~/covered/ && $6~/covered/' Ping_1200bp_status.txt > Ping_1200bp_status.txt.insertion.list
awk '$5!~/covered/ && $6~/covered/' Ping_1200bp_status.txt > Ping_1200bp_status.txt.No_1.list
awk '$5~/covered/ && $6!~/covered/' Ping_1200bp_status.txt > Ping_1200bp_status.txt.No_2.list
awk '$5!~/covered/ && $6!~/covered/' Ping_1200bp_status.txt > Ping_1200bp_status.txt.No_3.list
#final list of strain having Ping 1200
cat Ping_1200bp_status.txt.insertion.list Ping_1200bp_status.txt.No_1.list Ping_1200bp_status.txt.No_2.list > Ping_1200bp_status.insertion_No1_2.txt
cut -f2 Ping_1200bp_status.insertion_No1_2.txt > Ping_1200bp_status.insertion_No1_2.acc.txt
#all these 22 strain have new
python ~/BigData/software/bin/listdiff.py Ping_1200bp_status.insertion_No1_2.acc.txt ../../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt
awk '{print $1"\tChr13\t1200\t1203\t+"}' Ping_1200bp_status.insertion_No1_2.txt > Ping_1200bp_status.insertion_No1_2.PreGFF.list

echo "still missing after recall"
cat Ping_*_recall/*_status.insertion_No1_2.txt | cut -f2| sort | uniq > Ping_ALL_recall.insertion_No1_2.txt
python ~/BigData/software/bin/listdiff.py Ping_ALL_recall.insertion_No1_2.txt ../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt | grep "list2" | cut -d" " -f4 | awk '{print $1"\t"$1}' > Ping_ALL_recall.still_missing.txt
python Sub_matrix.py Ping_ALL_recall.still_missing.txt ../Zero_mPing_Strain/ping_3k_NM2.txt | sort -k2,2nr > Ping_ALL_recall.still_missing.ping_3k_NM2.txt
python sum_pop_distri_general.py --input Ping_ALL_recall.still_missing.txt

echo "echo Ping_5340_recall"
mkdir Ping_5340_recall
mkdir Ping_5340_recall/Ping_test_Round_Pre
python ReNameSRA_subset.py --input Ping_test.5340.list
cut -f2,5 Ping_test.5340.list.download.list | uniq | sort | uniq | sed 's/IRIS/IRIS_/' > Ping_test.5340.list.acc.txt
cut -f2 Ping_test.5340.list.acc.txt | awk '{print "cp Ping_3230_recall/Ping_Depth_Psuedo_Ping_bam/"$1"_Pseudo.NM2.bam* ./Ping_5340_recall/Ping_test_Round_Pre/"}' > Ping_test.5340.cp.sh
cp Ping_3230_recall/Ping_Round3_Pseudo_RF.fa Ping_5340_recall/Ping_test_Round_Pre/
#
mkdir Ping_test
cd Ping_test
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470332*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS470503*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469448*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469545*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS469811*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468782*.fastq.gz ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/ERS468500*.fastq.gz ./
cd ..
#Round0
mkdir Ping_test_Round0
cd Ping_test_Round0
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_5340_recall/Ping_test/*.gz ./
cd ..
cat up_round0.fa ping_trun.fa down_round0.fa > Ping_Round0_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round0_Pseudo.fa > Ping_Round0_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round0_Pseudo.fa
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round0 --genome Ping_Round0_Pseudo.fa > log 2>&1 &
#assemble
mkdir Ping_test_local_assembly
cd Ping_test_local_assembly
cp ../../Ping_3230_recall/Ping_test_local_assembly/Get_List_Raw_Fastq* ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_5340_recall/Ping_test_Round0/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round0 > log 2>&1 &
#Round1
cat up_round1.fa ping_trun.fa down_round1.fa > Ping_Round1_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round1_Pseudo.fa > Ping_Round1_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round1_Pseudo.fa
mkdir Ping_test_Round1
cd Ping_test_Round1
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_5340_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round1 --genome Ping_Round1_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_5340_recall/Ping_test_Round1/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round1 > log 2>&1 &
#Round2
cat up_round2.fa ping_trun.fa down_round2.fa > Ping_Round2_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round2_Pseudo.fa > Ping_Round2_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round2_Pseudo.fa
mkdir Ping_test_Round2
cd Ping_test_Round2
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_5340_recall/Ping_test/*.gz ./
cd ..  
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round2 --genome Ping_Round2_Pseudo.fa > log 2>&1 &
#assemble
cd Ping_test_local_assembly
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_5340_recall/Ping_test_Round2/ ./
python Get_List_Raw_Fastq_runner_Ping.py --input Ping_test_Round2 > log 2>&1 &
#Round3, just for building pseudogenome
cat up_round3.fa ping_trun.fa down_round3.fa > Ping_Round3_Pseudo.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo.fa > Ping_Round3_Pseudo_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo.fa
cat up_round3.fa down_round3.fa > Ping_Round3_Pseudo_noPing.fa
perl ~/BigData/software/bin/fastaDeal.pl --reform line50 Ping_Round3_Pseudo_noPing.fa > Ping_Round3_Pseudo_noPing_RF.fa
/opt/linux/centos/7.x/x86_64/pkgs/bwa/0.7.12/bin/bwa index Ping_Round3_Pseudo_noPing.fa
mkdir Ping_test_Round3
cd Ping_test_Round3
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_5340_recall/Ping_test/*.gz ./
cd ..
python Run_Map_multi_sample.py --fastq_dir Ping_test_Round3 --genome Ping_Round3_Pseudo.fa > log 2>&1 &
#map to pseudo with ping
mkdir Ping_Depth_Psuedo_Ping_bam
cd Ping_Depth_Psuedo_Ping_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_Ping_bam --genome Ping_Round3_Pseudo.fa > log 2>&1 &
#map to pseduo without ping
mkdir Ping_Depth_Psuedo_noPing_bam
cd Ping_Depth_Psuedo_noPing_bam
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_missed_indica_pseudogenome/Ping_Depth/*.fastq.gz ./
python Run_Map_multi_sample.py --fastq_dir Ping_Depth_Psuedo_noPing_bam --genome Ping_Round3_Pseudo_noPing.fa > log 2>&1 &
echo "Ping 5340 bp status, Ping_up:928-2555, Ping_up:928-929"
python mPing_Boundary_Coverage_Ping_5340bp.py --bam_ref Ping_Depth_Psuedo_noPing_bam --bam_pseudo Ping_Depth_Psuedo_Ping_bam > Ping_5340bp_status.txt
#23
awk '$5~/covered/ && $6~/covered/' Ping_5340bp_status.txt > Ping_5340bp_status.txt.insertion.list
#12
awk '$5!~/covered/ && $6~/covered/' Ping_5340bp_status.txt > Ping_5340bp_status.txt.No_1.list
#7
awk '$5~/covered/ && $6!~/covered/' Ping_5340bp_status.txt > Ping_5340bp_status.txt.No_2.list
awk '$5!~/covered/ && $6!~/covered/' Ping_5340bp_status.txt > Ping_5340bp_status.txt.No_3.list
#final list of strain having Ping 5340
cat Ping_5340bp_status.txt.insertion.list Ping_5340bp_status.txt.No_1.list Ping_5340bp_status.txt.No_2.list > Ping_5340bp_status.insertion_No1_2.txt
#this Ping is called in RelocaTE2: Chr11	ERS468796	RelocaTE_i	25822230	25822232
#31 is called in 3k genome
#Chr11   25822230        25822232        Chr11:25822230  +       31      0.171270718232
grep "25822230" ../../High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.gff | cut -f2 > Ping_5340bp_status.RelocaTE2.known.list
python ~/BigData/software/bin/listdiff.py Ping_5340bp_status.RelocaTE2.known.list Ping_5340bp_status.insertion_No1_2.txt > Ping_5340bp_status.insertion_No1_2.compare.list
cut -f2 Ping_5340bp_status.insertion_No1_2.txt > Ping_5340bp_status.insertion_No1_2.acc.txt
python ~/BigData/software/bin/listdiff.py ../../Zero_mPing_Strain/RelocaTE2_Depth_Ping.Only.txt Ping_5340bp_status.insertion_No1_2.acc.txt | grep "shared"
#final list have four new strain have this Ping
Ping_5340bp_status.insertion_No1_2.New.txt
#make list for prepare GFF
awk '{print $1"\tChr11\t25822230\t25822232\t+"}' Ping_5340bp_status.insertion_No1_2.New.txt > Ping_5340bp_status.insertion_No1_2.New.PreGFF.list

echo "echo Ping_1479_2_recall: same with 1479 we have"
mkdir Ping_1479_2_recall
mkdir Ping_1479_2_recall/Ping_test_Round_Pre
python ReNameSRA_subset.py --input Ping_test.1479_2.list
cut -f2,5 Ping_test.1479_2.list.download.list | uniq | sort | uniq | sed 's/IRIS/IRIS_/' > Ping_test.1479_2.list.acc.txt
cut -f2 Ping_test.1479_2.list.acc.txt | awk '{print "cp Ping_3230_recall/Ping_Depth_Psuedo_Ping_bam/"$1"_Pseudo.NM2.bam* ./Ping_1479_2_recall/Ping_test_Round_Pre/"}' > Ping_test.1479_2.cp.sh
cp Ping_3230_recall/Ping_Round3_Pseudo_RF.fa Ping_1479_2_recall/Ping_test_Round_Pre/

echo "Final add list"
#Chr3    ERS469922       RelocaTE_i      33213691        33213693        .       -       .       ID=repeat_Chr3_33213691_33213693;Strain=ERS469922;TSD=TAA;
#Note=Non-reference, not found in reference;Right_junction_reads:1;Left_junction_reads:1;Right_support_reads:3;Left_support_reads:1;
cat Ping_*_recall/*.PreGFF.list > Ping_ALL_recall.PreGFF.list
awk '{print $2"\t"$1"\tRelocaTE_i\t"$3"\t"$4"\t.\t+\t.\tID=repeat_"$2"_"$3"_"$4";Strain="$1";TSD=TAA;Note=Non-reference, not found in reference;Right_junction_reads:5;Left_junction_reads:5;Right_support_reads:5;Left_support_reads:5;"}' Ping_ALL_recall.PreGFF.list > Ping_ALL_recall.PreGFF.GFF

