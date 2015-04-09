#!/usr/bin/perl
use Getopt::Long;
use File::Basename;
use FindBin qw ($Bin);

GetOptions (\%opt,"ref:s","lib:s","group:s","project:s","help");


my $help=<<USAGE;
perl $0 --ref /rhome/cjinfeng/HEG4_cjinfeng/MappingReads/input/MSU_r7.fa --lib in_libs.EG4_CLEAN.csv --group in_groups.EG4_CLEAN.csv --project EG4_CLEAN
USAGE


if ($opt{help} or keys %opt < 1){
    print "$help\n";
    exit();
}

$opt{project} ||= "map";

my $reflib=readlib($opt{lib});
my $refgroup=readgroup($opt{group});
my $script="/rhome/cjinfeng/HEG4_cjinfeng/MappingReads/bin/step1_Mapping_large.pl";

open OUT, ">$opt{project}.sh" or die "$!";
foreach my $read (sort keys %$refgroup){
   #print "$read\n";
   my $fq1=$read;
   my $fq2=$read;
   $fq1=~s/\?/1/;
   $fq2=~s/\?/2/;
   my $head=$read=~/gz$/ ? basename($read,".fq.gz") : basename($read,".fq");
   $head=~s/\_p*\?//;
   print "$head\n";
   #print "$fq1\n$fq2\n";
   #print "$refgroup->{$read}\t$reflib->{$refgroup->{$read}}->[0]\t$reflib->{$refgroup->{$read}}->[1]\n";
   my $min=$reflib->{$refgroup->{$read}}->[0]-7*$reflib->{$refgroup->{$read}}->[1];
   my $max=$reflib->{$refgroup->{$read}}->[0]+7*$reflib->{$refgroup->{$read}}->[1];
   $min = $min > 0 ? $min : 0;
   my $cmd="perl $script -ref $opt{ref} -1 $fq1 -2 $fq2 -min $min -max $max -cpu 30 -tool bwa -project $Bin/$head\.$opt{project}";
   print OUT "$cmd\n";
}
close OUT;

#####
#illuminaGAIIx_200_2.3,HEG4_RAW,HEG4,fragment,1,148,25,,,inward,0,0
#illuminaGAIIx_500,HEG4_RAW,HEG4,jumping,1,,,433,27,inward,0,0
sub readlib
{
my ($file)=@_;
my %hash;
open IN, "$file" or die "$!";
<IN>;
while(<IN>){
    chomp $_;
    next if ($_=~/^$/);
    my @unit=split(",",$_);
    $hash{$unit[0]}=$unit[3]=~/fragment/ ? [$unit[5],$unit[6]] : [$unit[7],$unit[8]];
}
close IN;
return \%hash;
}
 

#jump_500_P1,illuminaGAIIx_500,/rhome/cjinfeng/HEG4_cjinfeng/fastq/errorcorrection/soapec/HEG4_0_500bp/FC52_7_?.fq
sub readgroup
{
my ($file)=@_;
my %hash;
open IN, "$file" or die "$!";
<IN>;
while(<IN>){
    chomp $_;
    next if ($_=~/^$/);
    my @unit=split(",",$_);
    $hash{$unit[2]}=$unit[1];
}
close IN;
return \%hash;
}
 
