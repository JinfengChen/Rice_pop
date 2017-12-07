cp ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure5_speical_ping/special_ping.list ./
echo "get subbam for special ping locus"
python Check_subbam.py --input rice_line_ALL_3000.anno.list > log 2>&1 &
echo "check if any bam is empty"
python Check_bam_size.py --input stowaway_check
echo "check locus status, 1 if there is insertion at special locus"
python Check_Locus_Status.py --input stowaway_check > stowaway_check.status
awk '$2==1' stowaway_check.status > stowaway_check.status.insertion.list
echo "only B003 in special ping list but not in candidate stowaway insertion list because of low coverage (code 3)?. add B003 in insertion.list anyway"
python ~/BigData/software/bin/listdiff.py special_ping.list stowaway_check.status.insertion.list

