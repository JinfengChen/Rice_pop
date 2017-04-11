echo "test Ping loci read type: G or A"
python Ping_SNP_PE_locus_reads.py --input test_3k_Ping > log 2>&1 &

echo "rice 3k Ping loci read type: G or A"
python Ping_SNP_PE_locus_reads.py --input Rice3k_3000_RelocaTEi_Ping > log 2>&1 &
#G-Ping, 51
awk '$3>1' Rice3k_3000_RelocaTEi_Ping.Ping_Locus_16th_SNP.summary | wc -l
#A-Ping, 150
awk '$5>1' Rice3k_3000_RelocaTEi_Ping.Ping_Locus_16th_SNP.summary | wc -l
grep -v "Population" Rice3k_3000_RelocaTEi_Ping.Ping_Locus_16th_SNP.pop.summary | cut -f5 | perl ~/BigData/software/bin/numberStat.pl

