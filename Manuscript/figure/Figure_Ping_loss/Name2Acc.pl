#!/usr/bin/perl

use FindBin qw ($Bin);
use Getopt::Long;


GetOptions(\%opt,"list:s","input:s","output:s","help:s");

my $help=<<USAGE;
Get lines from input that match ids in list file
perl $0 -l id -i gene.summary -o id.summary > log  

USAGE

if (exists $opt{help} or keys %opt < 1){
   print $help;
   exit;
}


my $ref=readtable($opt{list});

#Accession       Pong    Pong_NonRef     Pong_Ref        Name    Origin  Class
#ERS467753_RelocaTEi     4       3       1       IRIS313-15896   Colombia        Indica
#ERS467754_RelocaTEi     5       5       0       IRIS313-15897   China   Indica
open IN, "$opt{input}" or die "$!";
open OUT, ">$opt{output}" or die "$!";
while(<IN>){
    chomp $_;
    next if ($_=~/^$/);
    if ($_=~/^Acc/){
        #print OUT "$_\n";
        next;
    }
    my @unit=split("\t",$_);
    if (exists $ref->{$unit[4]}){
       my @array =split("\_", $unit[0]);
       print OUT "$_\n";
    }
}
close IN;
close OUT;

#################

sub readtable
{
### store id into hash %id
my %hash;
open IN, "$opt{list}" or die "$!";
while(<IN>){
    chomp $_;
    next if ($_ eq "");
    my @unit=split("\t",$_); 
    my $id=$unit[0];
    $hash{$id}=1;
}
close IN;
return \%hash;
}
