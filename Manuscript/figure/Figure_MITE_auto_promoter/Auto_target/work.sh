echo "Harbinger"
python make_target_peps_general.py `pwd`/query `pwd`/Target `pwd`/reference/MSU7.fa Target_Run_Harbinger_MSU7
python make_BEDfile_all_protein_hits.py Target/Target_Run_Harbinger_MSU7_angiosperm_harbinger_tpase_angiosperm_harbinger_tpase_2017_03_15_153554 ./Target/all_pep-hits.bed ./reference/MSU7.fa ./Target/nonredundant_pep_union-10kb.fa ./Target/nonredundant_pep_union-hits.fa
python split_fasta.py ./Target/nonredundant_pep_union-10kb.fa ./Target/split
python make_cdhit-prot_sh.py ./Target/nonredundant_pep_union-hits.fa
sbatch cd-hit_nonredundant_pep_union-hits-90.sh
sbatch cd-hit_nonredundant_pep_union-hits-80.sh
python make_multi_seq_sum.py Target/nonredundant_pep_union-hits_c90.clstr
python make_multi_seq_sum.py Target/nonredundant_pep_union-hits_c80.clstr
perl make_multi_seq.pl Target/nonredundant_pep_union-10kb.fa Target/nonredundant_pep_union-hits_c90.clstr Target/nonredundant_pep_union-10kb_c90_multi 2
perl make_multi_seq.pl Target/nonredundant_pep_union-10kb.fa Target/nonredundant_pep_union-hits_c80.clstr Target/nonredundant_pep_union-10kb_c80_multi 2
python trim_flanks_directory.py Target/nonredundant_pep_union-10kb_c80_multi/ 5000
python make_mafft_pep-cluster_split_one_sh.py Target/nonredundant_pep_union-10kb_c80_multi/ '*trimmed-5000.fa' MSU7


echo "blast mping/ping/pong with candidate"
module load ncbi-blast/2.2.26
formatdb -i nonredundant_pep_union-10kb.fa -p F
blastall -p blastn -i ~/BigData/00.RD/RelocaTE_i/Simulation/Reference/mPing_Ping_Pong.fa -d nonredundant_pep_union-10kb.fa -o mPing.blast


echo "Marinar"
python make_target_peps_general.py `pwd`/query `pwd`/Target_Mariner `pwd`/reference/MSU7.fa Target_Run_Mariner_MSU7
sbatch Target_Run_Mariner_MSU7_angiosperm_mariner_tpase.sh
module load cd-hit/4.6.4
module load bedops/2.4.24
module load mafft
python Target_Pep_Pipe.py --input Target_Mariner/Target_Run_Mariner_MSU7_angiosperm_mariner_tpase_angiosperm_mariner_tpase_2017_03_16_124024

echo "Mutator"
sbatch pep.sh

echo "hAT"
sbatch pep.sh

echo "ORU_australia"
bash pep_ORU_Australia.sh
sbatch Target_Run_ORU_Australia_angiosperm_hAT_tpase.sh 
sbatch Target_Run_ORU_Australia_angiosperm_mutator_tpase.sh 
sbatch Target_Run_ORU_Australia_angiosperm_mariner_tpase.sh 
sbatch Target_Run_ORU_Australia_angiosperm_harbinger_tpase.sh 

echo "Run all genome in pipe: step1 and step2"
bash pep_DJ123.sh > log 2>&1 &


