/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11665.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11665.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11685.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11685.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11669.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11669.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11643.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11643.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11801.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11801.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11646.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11646.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11812.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11812.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-8326.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-8326.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11723.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11723.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11693.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11693.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11802.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11802.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11705.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11705.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11657.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11657.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11671.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11671.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11664.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11664.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11683.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11683.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11691.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11691.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11686.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11686.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11635.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-11635.actin.coverage.clean.txt
/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-8921.realigned.bam chr03:29071995-29077870 | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | /opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view -b | /rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools coverage -abam stdin -b /rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.actin.bed -d | awk '{print $1"\t"$2+$4"\t"$5}' > /bigdata/wesslerlab/shared/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/ping_coverage_3k/IRIS_313-8921.actin.coverage.clean.txt
