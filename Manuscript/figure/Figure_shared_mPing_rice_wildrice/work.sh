echo "link 3k mPing/Ping/Pong calls"
#Ping
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.gff ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL_Ref.gff ./
#50
cat Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#42
grep -v "ins" Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.gff | grep -v "singl" | grep -v "supporting_reads" > Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.high_conf.gff
cat Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.high_conf.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
python AlleleFrq.py --input Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.high_conf.gff | sort -k6,6n | awk '$6==1'
python AlleleFrq.py --input Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.high_conf.gff > Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.high_conf.frequency

#mPing
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff 
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL_Ref.gff ./
#9854
cat Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#1966
grep -v "ins" Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff | grep -v "singl" | grep -v "supporting_reads" > Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.high_conf.gff
cat Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.high_conf.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
python AlleleFrq.py --input Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.high_conf.gff | sort -k6,6n | awk '$6==1'
python AlleleFrq.py --input Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.high_conf.gff > Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.high_conf.frequency

#Pong
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.gff ./
ln -s ~/Rice/Rice_population_sequence/Rice_3000/analysis/High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL_Ref.gff ./
#596
cat Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#457
grep -v "ins" Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.gff | grep -v "singl" | grep -v "supporting_reads" > Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.high_conf.gff
cat Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.high_conf.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
python AlleleFrq.py --input Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.high_conf.gff | sort -k6,6n | awk '$6==1'
python AlleleFrq.py --input Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.high_conf.gff > Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.high_conf.frequency

echo "wildrice mPing/Ping/Pong"
#mPing
python RunRelocaTEi_CombinedGFF_mPing.py --input fq_RelocaTE2_mPing
#265
cat fq_RelocaTE2_mPing.CombinedGFF.ALL.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#156
grep -v "ins" fq_RelocaTE2_mPing.CombinedGFF.ALL.gff | grep -v "singl" | grep -v "supporting_reads" > fq_RelocaTE2_mPing.CombinedGFF.ALL.high_conf.gff
cat fq_RelocaTE2_mPing.CombinedGFF.ALL.high_conf.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#frequency
python AlleleFrq.py --input fq_RelocaTE2_mPing.CombinedGFF.ALL.high_conf.gff | sort -k1,1 -k2,2n > fq_RelocaTE2_mPing.CombinedGFF.ALL.high_conf.frequency

#Ping
python RunRelocaTEi_CombinedGFF_mPing.py --input fq_RelocaTE2_Ping
#265
cat fq_RelocaTE2_Ping.CombinedGFF.ALL.gff |  sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#160
grep -v "ins" fq_RelocaTE2_Ping.CombinedGFF.ALL.gff | grep -v "singl" | grep -v "supporting_reads" > fq_RelocaTE2_Ping.CombinedGFF.ALL.high_conf.gff
cat fq_RelocaTE2_Ping.CombinedGFF.ALL.high_conf.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l

#Pong
python RunRelocaTEi_CombinedGFF_mPing.py --input fq_RelocaTE2_Pong
#169
cat fq_RelocaTE2_Pong.CombinedGFF.ALL.gff |  sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#95
grep -v "ins" fq_RelocaTE2_Pong.CombinedGFF.ALL.gff | grep -v "singl" | grep -v "supporting_reads" > fq_RelocaTE2_Pong.CombinedGFF.ALL.high_conf.gff
cat fq_RelocaTE2_Pong.CombinedGFF.ALL.high_conf.gff | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#frequency
python AlleleFrq.py --input fq_RelocaTE2_Pong.CombinedGFF.ALL.high_conf.gff | sort -k1,1 -k2,2n > fq_RelocaTE2_Pong.CombinedGFF.ALL.high_conf.frequency

echo "overlap between wild rice and rice mPing"
#30 mPing
bedtools window -w 10 -a fq_RelocaTE2_mPing.CombinedGFF.ALL.high_conf.gff -b Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff -u | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#2 Ping
bedtools window -w 10 -a fq_RelocaTE2_mPing.CombinedGFF.ALL.high_conf.gff -b Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.gff -u | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#1 Pong
bedtools window -w 10 -a fq_RelocaTE2_mPing.CombinedGFF.ALL.high_conf.gff -b Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.gff -u | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq | wc -l
#20 Pong
bedtools window -w 10 -a fq_RelocaTE2_Pong.CombinedGFF.ALL.high_conf.gff -b Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.gff -u | sort -k1,1 -k4,4n | awk '{print $1":"$4"-"$5}'| uniq | sort | uniq

echo ""
#6 mPing >= 1000 strains
awk '$6>=1000' Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.merge.frequency | wc -l
bedtools window -w 10 -a fq_RelocaTE2_mPing.CombinedGFF.ALL.high_conf.gff -b Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.merge.frequency | awk -F"\t" '$15>1000'| cut -f13 | uniq | sort | uniq
#2 pong >= 1000 strains
awk '$6>=1000' Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.merge.frequency
bedtools window -w 10 -a fq_RelocaTE2_Pong.CombinedGFF.ALL.high_conf.gff -b Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.merge.frequency | awk -F"\t" '$15>1000'| cut -f13 | uniq | sort | uniq

