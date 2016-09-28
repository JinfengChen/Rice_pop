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

