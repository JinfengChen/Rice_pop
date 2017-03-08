echo "30 rufipogon 16th SNP"
python Ping_SNP.py --input fq_RelocaTE2_Ping > log 2>&1 &
python Ping_SNP_PE.py --input fq_RelocaTE2_Ping > log 2>&1 &
python Pong_mpileup.py --input fq_RelocaTE2_Pong > log 2>&1 &
python mPing_mpileup.py --input fq_RelocaTE2_mPing > log 2>&1 &

echo "446 rufipgon 16th SNP"
python Ping_SNP.py --input Wildrice_fastq_RelocaTEi_Ping > log 2>&1 &

echo "3000 rice 16th SNP"
python Ping_SNP.py --input Rice3k_3000_RelocaTEi_Ping > log 2>&1 &
python Pong_mpileup.py --input Rice3k_3000_RelocaTEi_Pong > log 2>&1 &
python mPing_mpileup.py --input Rice3k_3000_RelocaTEi_mPing > log 2>&1 &


echo "ping and ping SNP"
awk -F"\t" '$8>0' rice_line_ALL_3000.anno.landrace.list > rice_line_ALL_3000.anno.landrace.ping.list
python convert_table_acc2name.py --input run_ping_SNP.rice_3000.16th_SNP.summary
awk -F"\t" '$4>1' run_ping_SNP.rice_3000.16th_SNP.summary.acc2name.txt > run_ping_SNP.rice_3000.16th_SNP.summary.acc2name.PingA.txt
cut -f1 rice_line_ALL_3000.anno.landrace.ping.list | grep -v "Taxa" > rice_line_ALL_3000.anno.landrace.ping.list.id
cut -f1 run_ping_SNP.rice_3000.16th_SNP.summary.acc2name.PingA.txt | grep -v "Taxa" > run_ping_SNP.rice_3000.16th_SNP.summary.acc2name.PingA.txt.id
