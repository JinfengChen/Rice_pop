echo "30 rufipogon 16th SNP"
python Ping_SNP.py --input fq_RelocaTE2_Ping > log 2>&1 &
python Ping_SNP_PE.py --input fq_RelocaTE2_Ping > log 2>&1 &
python Ping_SNP_PE_asm.py --input fq_RelocaTE2_Ping > log 2>&1 &
python merge_assembly.py --input fq_RelocaTE2_Ping_NM2_PE_assembly
python Pong_mpileup.py --input fq_RelocaTE2_Pong > log 2>&1 &
python mPing_mpileup.py --input fq_RelocaTE2_mPing > log 2>&1 &

echo "446 rufipgon 16th SNP"
python Ping_SNP.py --input Wildrice_fastq_RelocaTEi_Ping > log 2>&1 &

echo "3000 rice 16th SNP"
python Ping_SNP.py --input Rice3k_3000_RelocaTEi_Ping > log 2>&1 &
python Ping_SNP_PE.py --input Rice3k_3000_RelocaTEi_Ping > log 2>&1 &
python Pong_mpileup.py --input Rice3k_3000_RelocaTEi_Pong > log 2>&1 &
python mPing_mpileup.py --input Rice3k_3000_RelocaTEi_mPing > log 2>&1 &


echo "ping and ping SNP"
awk -F"\t" '$8>0' rice_line_ALL_3000.anno.landrace.list > rice_line_ALL_3000.anno.landrace.ping.list
python convert_table_acc2name.py --input run_ping_SNP.rice_3000.16th_SNP.summary
awk -F"\t" '$4>1' run_ping_SNP.rice_3000.16th_SNP.summary.acc2name.txt > run_ping_SNP.rice_3000.16th_SNP.summary.acc2name.PingA.txt
cut -f1 rice_line_ALL_3000.anno.landrace.ping.list | grep -v "Taxa" > rice_line_ALL_3000.anno.landrace.ping.list.id
cut -f1 run_ping_SNP.rice_3000.16th_SNP.summary.acc2name.PingA.txt | grep -v "Taxa" > run_ping_SNP.rice_3000.16th_SNP.summary.acc2name.PingA.txt.id

echo "ping reads"
python convert_table_acc2name.py --input Rice3k_3000_RelocaTEi_Ping.Ping_SNP_reads.sum.txt
sort Rice3k_3000_RelocaTEi_Ping.Ping_SNP_reads.sum.txt.acc2name.txt > Rice3k_3000_RelocaTEi_Ping.Ping_SNP_reads.sum.txt.acc2name_sorted.txt
awk -F"\t" '$2>1' Rice3k_3000_RelocaTEi_Ping.Ping_SNP_reads.sum.txt.acc2name.txt | cut -f1 > Rice3k_3000_RelocaTEi_Ping.Ping_SNP_reads.sum.txt.acc2name.Ping_reads.txt
paste Rice3k_3000_RelocaTEi_Ping.Ping_SNP_reads.sum.txt.acc2name_sorted.txt rice_line_ALL_3000.anno.landrace.list > Rice3k_3000_RelocaTEi_Ping.Ping_SNP_reads.sum.txt.acc2name_sorted.merged.txt
python sum_pop_distri.py --input Rice3k_3000_RelocaTEi_Ping.Ping_SNP_reads.sum.txt.acc2name_sorted.merged.txt
awk -F'\t' '$3>=0.1' ../Figure_copy_number_depth/Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.mapped_depth.txt | grep -v "Taxa" | cut -f1 > Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.mapped_depth.txt.id
python listdiff.py Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.mapped_depth.txt.id rice_line_ALL_3000.anno.landrace.ping.list.id | grep "list1" | cut -d" " -f4 > Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.mapped_depth.only.id

