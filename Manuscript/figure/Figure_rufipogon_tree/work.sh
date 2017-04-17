awk '{print $1"\t"$2"\t"$3"\t"$4"\t"$5"\tblack"}' Rufipogon_50_RelocaTE2.mPing_Ping_Pong.copy.depth.txt > Rufipogon_50_RelocaTE2.mPing_Ping_Pong.copy.depth.color.txt
sed 's/_hap0//g' RAxML_bootstrap.Wildrice_Outgroup_SNP.raxml.tree > RAxML_bootstrap.Wildrice_Outgroup_SNP.raxml.clean.tree
python Draw_Nexus_Tree.py --input RAxML_bootstrap.Wildrice_Outgroup_SNP.raxml.tree --anno Rufipogon_50_RelocaTE2.mPing_Ping_Pong.copy.depth.group.txt --color 7 --trait 2,3,4 --output Rufipogon_50_RelocaTE2.mPing_Ping_Pong
cat Rufipogon_50_RelocaTE2.mPing_Ping_Pong.R | R --slave

#rufipgon_48
sed 's/_hap0//g' RAxML_bipartitions.Wildrice_Outgroup_rufi48_Hom_norepeat_SNP_qsub.raxml_BS.tree > RAxML_bipartitions.Wildrice_Outgroup_rufi48_Hom_norepeat_SNP_qsub.raxml_BS.clean.tree
python add_group_color.py --input Rufipogon_57_RelocaTE2.mPing_Ping_Pong.copy.depth.txt --group Rufipogon.group.color.txt
python Draw_Nexus_Tree.py --input RAxML_bipartitions.Wildrice_Outgroup_rufi48_Hom_norepeat_SNP_qsub.raxml_BS.clean.tree --anno Rufipogon_57_RelocaTE2.mPing_Ping_Pong.copy.depth.group.txt --color 7 --trait 2,3,4 --output Rufipogon_57_RelocaTE2.mPing_Ping_Pong
cat Rufipogon_57_RelocaTE2.mPing_Ping_Pong.R | R --slave

