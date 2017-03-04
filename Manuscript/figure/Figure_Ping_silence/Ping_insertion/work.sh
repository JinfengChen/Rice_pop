echo "fake genome and flank"
python Pseudo_TEinsertion_Genome.py --repeat mPing_Ping_Pong.fa --gff nivara_IRGC105327.Ping.gff --genome MSU_r7.fa
awk '{print $1":"$4".."$5"\tping\t+"}' MSU_r7.Pseudo_mPing.gff > MSU_r7.Pseudo_mPing.plus.list
awk '{print $1":"$4".."$5"\tping\t-"}' MSU_r7.Pseudo_mPing.gff > MSU_r7.Pseudo_mPing.minus.list
python mPing_flank.py --list MSU_r7.Pseudo_mPing.plus.list --fasta mPing_Ping_Pong.fa --genome MSU_r7.Pseudo_mPing.fa --output mPing_flanking_1000_plus.fa
python mPing_flank.py --list MSU_r7.Pseudo_mPing.minus.list --fasta mPing_Ping_Pong.fa --genome MSU_r7.Pseudo_mPing.fa --output mPing_flanking_1000_minus.fa
