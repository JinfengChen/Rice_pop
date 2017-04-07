cat mPing_Ping_Pong_variation.R | R --slave
python Group_Percent_Variation.py --input rice_line_ALL_3000.anno.landrace.list.txt > mPing_Ping_Pong_percent.txt
cat mPing_Ping_Pong_percent.R | R --slave

