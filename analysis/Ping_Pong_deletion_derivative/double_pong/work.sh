echo "repeatmasker"
RepeatMasker --species rice ping.fa
RepeatMasker --species rice pong.fa

echo "reference IGV"
picard CreateSequenceDictionary R=pong.fa O=pong.fa.dict
picard CreateSequenceDictionary R=ping.fa O=ping.fa.dict

echo "pong bam to fq"
samtools view -b -f 4 ~/BigData/01.Rice_genomes/A123/00.Bam/A123_MSU7_BWA/A123_0.clean.A123_CLEAN.bam > A123_unmapped.bam
samtools sort -n A123_unmapped.bam A123_unmapped.bayname
bedtools bamtofastq -i A123_unmapped.bayname.bam -fq A123_unmapped_1.fq -fq2 A123_unmapped_2.fq
intersectBed -abam ~/BigData/01.Rice_genomes/A123/00.Bam/A123_MSU7_BWA/A123_0.clean.A123_CLEAN.bam -b Pong_2k.gff > A123_Pong.bam
samtools sort -n A123_Pong.bam A123_Pong.byname
bedtools bamtofastq -i A123_Pong.byname.bam -fq A123_Pong_1.fq -fq2 A123_Pong_2.fq
qsub A123.RelocaTEi_Ping.sh

echo "rice 3000"
#prepare fastq
awk '{print $1":"$4"-"$5}' Pong_2k.gff
python Rice3k_download_bam_Pong.py --input test.list
python Rice3k_download_bam_Pong.py --input rice_line_ALL_3000.anno.list
python Rice3k_download_bam_Pong_failed.py --input rice_line_ALL_3000.anno.list
#run RelocaTE2
python Rice3k_RelocaTE2_Pong.py --input pong_3k
grep "IRIS" -v pong_3k_RelocaTE2.run.sh > test.run.sh
grep "IRIS" pong_3k_RelocaTE2.run.sh > test.run1.sh
perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 80 --lines 5 --interval 120 --resource nodes=1:ppn=16,walltime=10:00:00,mem=30G --convert no test.run.sh > log4 &
perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 80 --lines 50 --interval 120 --resource nodes=1:ppn=16,walltime=10:00:00,mem=30G --convert no test.run1.sh > log4 &
#summary double pong group
ls -d *_RelocaTE2| wc -l
cat pong_3k_RelocaTE2/*_RelocaTE2/repeat/results/ALL.all_nonref_insert.gff | grep "4987" -v | cut -f3 | sed 's/\_pong\_RelocaTE2//' > Double_Pong_new.id.list
cat pong_3k_RelocaTE2/*_RelocaTE2/repeat/results/ALL.all_nonref_insert.gff | grep "4987" | cut -f3 | sed 's/\_pong\_RelocaTE2//' > Double_Pong.id.list
python summary_list.py --input Double_Pong_new.id.list
python summary_list.py --input Double_Pong.id.list

#RelocaTE2 call
sort -k1,1 -k4,4n ~/Rice/Rice_population_sequence/Rice_3000/analysis/High_Ping_Indonesia_group/Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL_Ref.gff | grep "12415640" > Double_Pong.RelocaTE2_call.gff
cut -f2 Double_Pong.RelocaTE2_call.gff > Double_Pong.RelocaTE2_call.id
python summary_list_RelocaTE2.py --input Double_Pong.RelocaTE2_call.id
#File1 only 14
#File2 only 2
#Shared 133
python listdiff2.py Double_Pong.RelocaTE2_call.id.list Double_Pong.id.list

