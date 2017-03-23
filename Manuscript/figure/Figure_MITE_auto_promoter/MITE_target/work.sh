
python make_target_nonauto_general_redo.py `pwd`/query/ `pwd`/Target `pwd`/reference/MSU7.fa Target_Run_MITE_MSU7


sort -k8,8rn Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.txt | awk '$6>200' | grep "rice_3_41532"
sort -k8,8rn Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.txt | awk '$6>200' | grep "rice_2_73170"
sort -k8,8rn Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.txt | awk '$6>200' | grep "rice_1_128219"

echo "summary MITE"
python Select_Multiple_HighIdentity.py --input Target/Target_Run_MITE_MSU7_2017_03_15_143604 > log &

sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$5>=0.98'| cut -f4 | perl ~/BigData/software/bin/numberStat.pl 
sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$5>=0.96 && $5<=0.98'| cut -f4 | perl ~/BigData/software/bin/numberStat.pl 
sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$5>=0.94 && $5<=0.96'| cut -f4 | perl ~/BigData/software/bin/numberStat.pl 
sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$5>=0.92 && $5<=0.94'| cut -f4 | perl ~/BigData/software/bin/numberStat.pl 
sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$5>=0.90 && $5<=0.92'| cut -f4 | perl ~/BigData/software/bin/numberStat.pl 
sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$5>=0.88 && $5<=0.90'| cut -f4 | perl ~/BigData/software/bin/numberStat.pl 
sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$5>=0.86 && $5<=0.88'| cut -f4 | perl ~/BigData/software/bin/numberStat.pl

sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$4>=50' | wc -l
sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$4>=50 && $5>=0.95' > Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.brief.50_0.95.txt
sort -k5,5rn -k4,4n Target/Target_Run_MITE_MSU7_2017_03_19_154911.MITE_copy_identify.brief.txt | grep -v "Query"| awk '$4>=50 && $5>=0.95' > Target/Target_Run_MITE_MSU7_2017_03_19_154911.MITE_copy_identify.brief.50_0.95.txt

echo "Repeatmasker on MITE"
/opt/linux/centos/7.x/x86_64/pkgs/RepeatMasker/4-0-5/RepeatMasker -species rice -q -nolow -no_is -norna MSU7.MITEhunter.fasta.len800.fasta > log 2>&1 &
 
