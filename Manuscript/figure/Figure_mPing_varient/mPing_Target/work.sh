echo "download aus DJ123 and indica IR64"
#sbatch --array 1-2 down_qsub.sh
#gunzip -d os.dj123.cshl.draft.1.0.scaffold.fa.gz 
#mv os.dj123.cshl.draft.1.0.scaffold.fa DJ123.fa
#gunzip -d os.ir64.cshl.draft.1.0.scaffold.fa.gz 
#mv os.ir64.cshl.draft.1.0.scaffold.fa IR64.fa
#gunzip -d GCA_000817225.1_OR_W1943_genomic.fna.gz 
#mv GCA_000817225.1_OR_W1943_genomic.fna ORU_W1943.fa
#gunzip -d GCA_001551805.1_ASM155180v1_genomic.fna.gz 
#mv GCA_001551805.1_ASM155180v1_genomic.fna ORU_Australia.fa
#mv *.fa reference/

echo "run target"
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/MSU7.fa Target_Run_mPing_MSU7
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/IR64.fa Target_Run_mPing_IR64
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/OID.fa Target_Run_mPing_OID
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/DJ123.fa Target_Run_mPing_DJ123
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/ONI.fa Target_Run_mPing_ONI
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/ORU.fa Target_Run_mPing_ORU
#Australia wild rice TaxonA, showed introgression from indica/nivara group, should not use as wild rice. PMID:27889940
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/ORU_Australia.fa Target_Run_mPing_ORU_Australia
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/ORU_W1943.fa Target_Run_mPing_ORU_W1943
#rufipogon_30
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/Rufipogon_30_mPing.fa Target_Run_mPing_Rufipogon_30_mPing
#rice 3k
python make_target_nonauto_general_redo.py ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/query ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/Target ~/BigData/00.RD/Transposon_Oryza/OGE_genomes/mPing_Target/reference/rice3k.fa Target_Run_mPing_rice3k

ls ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure_mPing_varient/mPing_Target/reference/rice3k.fa.cut/rice3k.fa.* > rice3k.fa.list

echo "merge target candidate"
cat Target/Target_Run_mPing_*/mping_split1/mping_split1.flank_filter-1.2_under > Target_merge_elements/mPing_target_condidate.fa
python clean_target_candidate.py --input Target_merge_elements/mPing_target_condidate.fa
#remove OID1, ORU and ORU_W1943, these mPing have N.
muscle -in Target_merge_elements/mPing_target_condidate.clean.fa -out Target_merge_elements/mPing_target_condidate.clean.msa
cat ~/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa Target_merge_elements/mPing_target_condidate.clean.fa > Target_merge_elements/mPing_target_condidate.clean_withPing.fa
muscle -in Target_merge_elements/mPing_target_condidate.clean_withPing.fa -out Target_merge_elements/mPing_target_condidate.clean_withPing.msa

#rufipogon 30
perl ~/BigData/software/bin/getidseq.pl -l mPing_variants.list -f mPing_target_condidate.clean.fa -o mPing_variants.fa
cp ../Target/Target_Run_mPing_Rufipogon_30_mPing_2017_03_09_144419/mping_split1/mping_split1.flank_filter-1.2_under rufipogon_30.target.fa
cat rufipogon_30.target.fa mPing_variants.fa > rufipogon_30.target_mPing_class.fa
muscle -in rufipogon_30.target_mPing_class.fa -out rufipogon_30.target_mPing_class.msa

#rice3k
cd Target_merge_elements
cp ../Target/Target_Run_mPing_rice3k_2017_03_09_162828/mping_split1/mping_split1.flank_filter-2.0_under rice3k.target.fa
python ../clean_target_candidate_N.py --input rice3k.target.fa
cat rice3k.target.Nclean.fa mPing_variants.fa > rice3k.target.Nclean_mPing_class.fa



