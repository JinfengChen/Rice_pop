paste Transposon_mPing_Ping_Pong.3k_Ping.summary Transposon_mPing_Ping_Pong.3k_mPing.summary Transposon_mPing_Ping_Pong.3k_Pong.summary | cut -f1-4,9-11,16-21 | sort -k8,8nr | grep "Acc" > Transposon_mPing_Ping_Pong.summary.jinfeng.high_pong
paste Transposon_mPing_Ping_Pong.3k_Ping.summary Transposon_mPing_Ping_Pong.3k_mPing.summary Transposon_mPing_Ping_Pong.3k_Pong.summary | cut -f1-4,9-11,16-21 | sort -k8,8nr | awk '$8>=10' >> Transposon_mPing_Ping_Pong.summary.jinfeng.high_pong

echo "plot"

cat Rice_3k_distri.R | R --slave
#add zoom in test1.pdf to Rice_3k_distri.pdf.A in AI. 
cat test1.R | R --slave

