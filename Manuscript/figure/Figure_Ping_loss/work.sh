echo "convert strains name to accession number"
perl Name2Acc.pl -l Group1_Ping_loss.list -i Transposon_mPing_Ping_Pong.3k_mPing.summary -o Group1_Ping_loss.Acc.list
perl Name2Acc.pl -l Group1_Ping_loss.1Ping.list -i Transposon_mPing_Ping_Pong.3k_Ping.summary -o Group1_Ping_loss.1Ping.Acc.list:

#sub group comparision mPing.
#lots of mPing shared in group2 and in group3 and in group4
python Ping_matrix_by_list.py --input Group1_Ping_loss.Acc1.list --gff Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff --output Group1_Ping_loss.Acc1
python Ping_matrix_by_list.py --input Group1_Ping_loss.Acc2.list --gff Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff --output Group1_Ping_loss.Acc2
python Ping_matrix_by_list.py --input Group1_Ping_loss.Acc3.list --gff Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff --output Group1_Ping_loss.Acc3
python Ping_matrix_by_list.py --input Group1_Ping_loss.Acc4.list --gff Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff --output Group1_Ping_loss.Acc4
python Ping_matrix_by_list.py --input Group1_Ping_loss.Acc5.list --gff Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.gff --output Group1_Ping_loss.Acc5

#landrace group Ping
python Ping_matrix_by_list.py --input Ping_Landrace_group.list --gff Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.gff --output Ping_Landrace_group

