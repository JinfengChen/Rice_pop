#!/usr/bin/perl
=header
The scripts is designed to run bwa to map solexa sequencing read to reference genome.
Fastq file is split into small files and use qsub to run in biocluster. So just run *.sh in local machine. *.sh could be generate by runMapping.pl.
USE fullpath of files.
--ref:   reference sequence
--1:     paired read with -2, SRR034638_1.fastq
--2:     paired read with -1, SRR034638_2.fastq
--tool:  mapping tools: bwa, maq, ssaha, soap
-project: project name that used for result file 
=cut

use Getopt::Long;
use File::Basename;
use FindBin qw ($Bin);


my %opt;
GetOptions(\%opt,"ref:s","1:s","2:s","tool:s","min:s","max:s","cpu:s","bam","verbose","output:s","project:s","help");

if ($opt{help} or keys %opt < 1){
   print "Usage: perl $0 -ref fullpath/all.con -1 fullpath/1.fq -2 fullpath/2.fq -min 0 -max 500 -cpu 12 -tool bwa\n";
   exit();
}


$opt{tool} ||= "bwa";
$opt{cpu} ||=12;
$opt{min} ||= 0;
$opt{max} ||= 500; 

unless ($opt{project}){
    print "Need to specify project name: current folder/out\n";
    exit(2)
}

$opt{output} ="$opt{project}";
`mkdir $opt{output}` unless (-d $opt{output});


my $bwa="/opt/tyler/bin/";
my $soap="/usr/local/bin";
my $ssaha="/home/jfchen/software/ssaha2_v2.5.5_x86_64/";
my $maq="/opt/tyler/bin/maq";
my $fqsplit="/rhome/cjinfeng/software/bin/fastq_split.pl";
my $SAMtool="/usr/local/bin/samtools";
my $rmdup="/opt/picard/1.81/MarkDuplicates.jar";

if (exists $opt{1} and exists $opt{2}){
   if ($opt{tool}=~/bwa/){
      print "Run pair-end mapping by BWA!\n";
      unless (-e "$opt{ref}.sa"){
         `$bwa/bwa index $opt{ref} > $opt{project}.index.log 2> $opt{project}.index.log2`;
      }
      ### split into small files
      my $fqhead1;
      my $fqhead2;
      if ($opt{1}=~/\.gz$/){
         $fqhead1= $opt{1}=~/fastq\.gz$/ ? basename($opt{1},".fastq.gz") : basename($opt{1},".fq.gz");
         $fqhead2= $opt{2}=~/fastq\.gz$/ ? basename($opt{2},".fastq.gz") : basename($opt{2},".fq.gz");
      }else{
         $fqhead1= $opt{1}=~/fastq$/ ? basename($opt{1},".fastq") : basename($opt{1},".fq");
         $fqhead2= $opt{2}=~/fastq$/ ? basename($opt{2},".fastq") : basename($opt{2},".fq");
      } 
      my @split;
      push @split, "perl $fqsplit -s 1000000 -o $opt{output} $opt{1}";
      push @split, "perl $fqsplit -s 1000000 -o $opt{output} $opt{2}";
      my $cmd=join("\n",@split);
      writefile("$opt{project}.split.sh","$cmd\n");
      `perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --interval 120 $opt{project}.split.sh`;

      ### map small files
      my @map;
      my @fqs=sort glob("$opt{output}/*.f*q");
      for(my $i=0; $i<@fqs; $i+=2){
           print "$i\t$fqs[$i]\n";
           #my $prefix=substr(basename($fqs[$i]),0,3);
           my $temp=basename($fqs[$i]);
           my $prefix=$1 if ($temp=~/^(p\d+)\./);
           push @map, "$bwa/bwa aln -t 1 $opt{ref} $fqs[$i] > $fqs[$i].sai 2> $fqs[$i].bwa.log2";
           push @map, "$bwa/bwa aln -t 1 $opt{ref} $fqs[$i+1] > $fqs[$i+1].sai 2> $fqs[$i+1].bwa.log2";
           push @map, "$bwa/bwa sampe -a $opt{max} $opt{ref} $fqs[$i].sai $fqs[$i+1].sai $fqs[$i] $fqs[$i+1] > $opt{output}/$prefix.sam 2> $opt{output}/$prefix.sampe.log2";
      }
      my $cmd1=join("\n",@map);
      writefile("$opt{project}.map.sh","$cmd1\n");
      `perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --maxjob 30 --lines 3 --interval 120 --resource walltime=100:00:00 --convert no $opt{project}.map.sh`;

      ### merge and clean tmp files
      my @merge;
      unless (-e "$opt{output}.sam"){
          push (@merge, "head -n 12 $opt{output}/p00.sam > $opt{output}.sam");
          push (@merge, "cat $opt{output}/p*.sam | grep -v \"^@\" >> $opt{output}.sam");
      }
      #push (@merge, "head -n 12 $opt{output}/p00.sam > $opt{output}.header") unless (-e "$opt{output}.header");
      #push (@merge, "cat $opt{output}/p*.sam | grep -v \"^@\" > $opt{output}.temp.sam") unless (-e "$opt{output}.temp.sam");
      #push (@merge, "cat $opt{output}.header $opt{output}.temp.sam > $opt{output}.sam") unless (-e "$opt{output}.sam");
      push (@merge, "$SAMtool view -bS -o $opt{output}.raw.bam $opt{output}.sam > $opt{output}.convert.log 2> $opt{output}.convert.log2") unless (-e "$opt{output}.raw.bam");
      push (@merge, "$SAMtool sort -m 1000000000 $opt{output}.raw.bam $opt{output}.sort > $opt{output}.sort.log 2> $opt{output}.sort.log2") unless (-e "$opt{output}.sort.bam");
      push (@merge, "java -Xmx5G -jar $rmdup ASSUME_SORTED=TRUE REMOVE_DUPLICATES=TRUE VALIDATION_STRINGENCY=LENIENT INPUT=$opt{output}.sort.bam OUTPUT=$opt{output}.bam METRICS_FILE=$opt{output}.dupli > $opt{output}.rmdup.log 2> $opt{output}.rmdup.log2") unless (-e "$opt{output}.bam");
      my $cmd2=join("\n",@merge);
      writefile("$opt{project}.merge.sh","$cmd2\n");
      `perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --lines 6 --interval 120  --resource walltime=100:00:00,mem=10G --convert no $opt{project}.merge.sh`;

      ### clear tmp files
      my @clear;
      push @clear, "rm $opt{output}.sam $opt{output}.temp.sam $opt{output}.header $opt{output}.raw.bam $opt{output}.sort.bam";
      push @clear, "rm $opt{output}.*.log* $opt{1}.sai $opt{1}.bwa.log2 $opt{2}.sai $opt{2}.bwa.log2";
      push @clear, "rm $opt{output} $opt{output}.map.sh* $opt{output}.split.sh* $opt{output}.merge.sh* -R";
      my $cmd3=join("\n",@clear);
      writefile("$opt{project}.clear.sh","$cmd3\n");
      unless ($opt{verbose}){
          `perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --lines 3 --interval 120 --convert no $opt{project}.clear.sh`;
      }
=cut
      print "Align Read 1!\n";
      `$bwa/bwa aln -t $opt{cpu} $opt{ref} $opt{1} > $opt{1}.sai 2> $opt{1}.bwa.log2`;
      print "Align Read 2!\n";
      `$bwa/bwa aln -t $opt{cpu} $opt{ref} $opt{2} > $opt{2}.sai 2> $opt{2}.bwa.log2`;
      print "Pairing!\n";
      `$bwa/bwa sampe -a $opt{max} $opt{ref} $opt{1}.sai $opt{2}.sai $opt{1} $opt{2} > $opt{project}.sam 2> $opt{project}.sampe.log2`;
      print "SAM 2 BAM!\n";
      `$SAMtool view -bS -o $opt{project}.raw.bam $opt{project}.sam > $opt{project}.convert.log 2> $opt{project}.convert.log2`;
      print "Sort Bam!\n";
      `$SAMtool sort $opt{project}.raw.bam $opt{project}.sort > $opt{project}.sort.log 2> $opt{project}.sort.log2`;
      print "Remove duplicate!\n";
      `java -jar $rmdup ASSUME_SORTED=TRUE REMOVE_DUPLICATES=TRUE VALIDATION_STRINGENCY=LENIENT INPUT=$opt{project}.sort.bam OUTPUT=$opt{project}.bam METRICS_FILE=$opt{project}.dupli > $opt{project}.rmdup.log 2> $opt{project}.rmdup.log2`;
      unless ($opt{verbose}){
          `rm $opt{project}.sam $opt{project}.raw.bam $opt{project}.sort.bam`;
          `rm $opt{project}.*.log* $opt{project}.dupli $opt{1}.sai $opt{1}.bwa.log2 $opt{2}.sai $opt{2}.bwa.log2`;
      }
      print "Done!\n";
=cut
   }elsif($opt{tool}=~/soap/){ # soap
      print "Run pair-end mapping by soap!\n";
      unless (-e "$opt{ref}.index.sai"){
         `$soap/2bwt-builder $opt{ref} > $opt{project}.builder.log 2> $opt{project}.builder.log2`;
         `$SAMtool faidx $opt{ref}`; # generate $opt{ref}.fai used in samtools view
      }
      `$soap/soap -a $opt{1} -b $opt{2} -D $opt{ref}.index -o $opt{project}.soap.PE -2 $opt{project}.soap.SE -p $opt{cpu} -m $opt{min} -x $opt{max} > $opt{project}.soap.log 2> $opt{project}.soap.log2` if ($opt{max} < 2000);
      `$soap/soap -a $opt{1} -b $opt{2} -D $opt{ref}.index -o $opt{project}.soap.PE -2 $opt{project}.soap.SE -p $opt{cpu} -m $opt{min} -x $opt{max} -R > $opt{project}.soap.log 2> $opt{project}.soap.log2` if ($opt{max} >= 2000);
      #`cat $opt{project}.soap.PE $opt{project}.soap.SE > $opt{project}.soap`;
      if ($opt{bam}){
      print "Convert SOAP to SAM\n";
      `perl /opt/tyler/bin/soap2sam.pl $opt{project}.soap.SE > $opt{project}.soap.SE.sam`;
      `perl /opt/tyler/bin/soap2sam.pl -p $opt{project}.soap.PE > $opt{project}.soap.PE.sam`;
      print "Convert SAM to BAM, sort and merge\n";
      `$SAMtool view -bS -t $opt{ref}.fai -o $opt{project}.raw.SE.bam $opt{project}.soap.SE.sam > $opt{project}.convert.SE.log 2> $opt{project}.convert.SE.log2`;
      `$SAMtool sort $opt{project}.raw.SE.bam $opt{project}.SE.sort > $opt{project}.SE.sort.log 2> $opt{project}.SE.sort.log2`;
      `$SAMtool view -bS -t $opt{ref}.fai -o $opt{project}.raw.PE.bam $opt{project}.soap.PE.sam > $opt{project}.convert.PE.log 2> $opt{project}.convert.PE.log2`;
      `$SAMtool sort $opt{project}.raw.PE.bam $opt{project}.PE.sort > $opt{project}.PE.sort.log 2> $opt{project}.PE.sort.log2`;
      `$SAMtool merge -f $opt{project}.sort.bam $opt{project}.SE.sort.bam $opt{project}.PE.sort.bam`;  
      print "Remove duplicate!\n";
      `java -jar $rmdup ASSUME_SORTED=TRUE REMOVE_DUPLICATES=TRUE VALIDATION_STRINGENCY=LENIENT INPUT=$opt{project}.sort.bam OUTPUT=$opt{project}.bam METRICS_FILE=$opt{project}.dupli > $opt{project}.rmdup.log 2> $opt{project}.rmdup.log2`;
      }
      unless ($opt{verbose}){
          `rm $opt{project}.*.sam $opt{project}.raw.*.bam $opt{project}.*.sort.bam $opt{project}.sort.bam`;
          `rm $opt{project}.*.log* $opt{project}.dupli`;
          
      }
      print "Done!\n";
   }elsif($opt{tool}=~/maq/){ # maq
      ## build reference index
      unless (-e "$opt{ref}.bfa"){
         `$maq fasta2bfa $opt{ref} $opt{ref}.bfa`;
      }
      `$maq fastq2bfq $opt{1} $opt{1}.bfq` unless (-e "$opt{1}.bfq");
      `$maq fastq2bfq $opt{2} $opt{2}.bfq` unless (-e "$opt{2}.bfq");
      `$maq match -a $opt{max} $opt{project}.Maq.map $opt{ref}.bfa $opt{1}.bfq $opt{2}.bfq`;
      `$maq mapview $opt{project}.Maq.map > $opt{project}.Maq.map.view`; 
   }
}



sub writefile
{
my ($file,$line)=@_;
open WR, ">$file" or die "$!";
     print WR "$line";
close WR;
}


