cp ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/pong_coverage_rice3000_MSU7.matrix.header.ordered.header.txt ./
cp ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/actin_coverage_rice3000_MSU7.matrix.header.ordered.header.txt ./
cp ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_rice3000_MSU7.matrix.header ./
sed 's/.actin.coverage.clean.txt//g' actin_coverage_rice3000_MSU7.matrix.header.ordered.header.txt > actin_3k.txt
sed 's/.ping.coverage.clean.txt//g' ping_coverage_rice3000_MSU7.matrix.header > ping_3k.txt
sed 's/.pong.coverage.clean.txt//g' pong_coverage_rice3000_MSU7.matrix.header.ordered.header.txt > pong_3k.txt

echo "Zero mPing: 220 strains; Zero Ping: 2749 strains; Zero Pong: 18 strains"
awk -F"\t" '$7==0' ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure2_3000_rice_tree/rice_line_ALL_3000.anno.landrace.list | wc -l
awk -F"\t" '$7==0' ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure2_3000_rice_tree/rice_line_ALL_3000.anno.landrace.list |cut -f1 > Zero_mPing_strains.list
awk -F"\t" '$9==0' ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure2_3000_rice_tree/rice_line_ALL_3000.anno.landrace.list | cut -f1 > Zero_Pong_strains.list
awk -F"\t" '$8==0' ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure2_3000_rice_tree/rice_line_ALL_3000.anno.landrace.list | cut -f1 > Zero_Ping_strains.list
cat Zero_mPing_plot.R | R --slave
cat Zero_Ping_plot.R | R --slave
cat Zero_Pong_plot.R | R --slave

echo "testing mismatch number, 0"
tail -n 50 ~/Rice/Rice_population_sequence/Rice_3000/analysis/Zero_mPing_Strain/Zero_Ping_strains.list > rice_line_ALL_3000.anno.list.zero_ping50
cat ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_rice3000_MSU7.matrix.header | sed 's/.ping.coverage.clean.txt//g' > ping_50.txt
cat ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/pong_coverage_rice3000_MSU7.matrix.header.ordered.header.txt | sed 's/.pong.coverage.clean.txt//g' > pong_50.txt

echo "use RelocaTE2 bam"
cat ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_rice3000_MSU7.matrix.header | sed 's/.ping.coverage.clean.txt//g' > ping_3k_NM0.txt
cat ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/pong_coverage_rice3000_MSU7.matrix.header.ordered.header.txt | sed 's/.pong.coverage.clean.txt//g' > pong_3k_NM0.txt
cat ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/actin_coverage_rice3000_MSU7.matrix.header.ordered.header.txt | sed 's/.actin.coverage.clean.txt//g' > actin_3k_NM0.txt
cat ~/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/mping_coverage_rice3000_MSU7.matrix.header.ordered.header.txt | sed 's/.mping.coverage.clean.txt//g' > mping_3k_NM0.txt
cat Zero_Ping_plot.R | R --slave

