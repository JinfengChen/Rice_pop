perl /rhome/cjinfeng/software/bin/fastaDeal.pl --pat chr01 /rhome/cjinfeng/BigData/00.RD/GenomeAlign/Lastz/input/HEG4_ALLPATHLG_v1.chr.fasta > HEG4.Chr01.fa
/opt/tyler/bin/bwa index HEG4.Chr01.fa > log 2> log2 &


echo "special ping in stowaway with 1000 flanking sequence"
python mPing_flank.py --list ping.list --fasta Ping_S.fa
/opt/tyler/bin/bwa index Ping_S_flanking_1000.fa

echo "new ping in three strain"
python mPing_flank.py --list new_ping.list --fasta mPing_Ping_Pong.fa --output new_ping_pong_flanking_1000.fa
/opt/tyler/bin/bwa index new_ping_pong_flanking_1000.fa > log 2> log2 &


