#python Rice3k_copy_number_depth.py > log 2>&1 &
#python merge_table.py > Ping_Pong_CopyNumber.txt
echo "2 mismatch allowed, using 260-4600 region to estimate"
python Rice3k_copy_number_depth.py --input fq_RelocaTE2_Ping_NM2 --output fq_RelocaTE2_Ping_NM2.Ping_copy.txt
python merge_table_ping_and_depth.py --input fq_RelocaTE2_Ping_NM2.Ping_copy.txt --depth rufipogon.bam.summary

echo "3000 Ping"
python Rice3k_copy_number_depth.py --input Rice3k_3000_RelocaTEi_Ping_NM2 --output Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.txt &
python merge_table_ping_and_depth_3k.py --input Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.txt --depth rice_3k_copy_number_depth.txt
#merge and compare with RelocaTE2
python merge_table_compare.py > Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.actin_depth.compare_RelocaTE2.txt
cat Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.actin_depth.compare_RelocaTE2.R| R --slave

#mapped depth
python merge_table_ping_and_depth_3k_mapped_depth.py --input Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.txt --depth rice_3k_depth.txt
python merge_table_compare_Ping.py > Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.mapped_depth.compare_RelocaTE2.txt
cat Rice3k_3000_RelocaTEi_Ping_NM2.Ping_copy.mapped_depth.compare_RelocaTE2.R| R --slave


echo "3000 Pong"
python Rice3k_copy_number_depth.py --input Rice3k_3000_RelocaTEi_Pong_NM2 --output Rice3k_3000_RelocaTEi_Pong_NM2.Pong_copy.txt &
python merge_table_ping_and_depth_3k_mapped_depth.py --input Rice3k_3000_RelocaTEi_Pong_NM2.Pong_copy.txt --depth rice_3k_depth.txt
python merge_table_compare_Pong.py > Rice3k_3000_RelocaTEi_Pong_NM2.Pong_copy.mapped_depth.compare_RelocaTE2.txt

echo "3000 mPing"
python Rice3k_copy_number_depth_mPing.py --input Rice3k_3000_RelocaTEi_mPing_NM2 --output Rice3k_3000_RelocaTEi_mPing_NM2.mPing_copy.txt &
python merge_table_ping_and_depth_3k_mapped_depth.py --input Rice3k_3000_RelocaTEi_mPing_NM2.mPing_copy.txt --depth rice_3k_depth.txt
python merge_table_compare_mPing.py > Rice3k_3000_RelocaTEi_mPing_NM2.mPing_copy.mapped_depth.compare_RelocaTE2.txt


echo "30 rufipogon Ping"
python Rice3k_copy_number_depth.py --input fq_RelocaTE2_Ping_NM2 --output fq_RelocaTE2_Ping_NM2.Ping_copy.txt &
python merge_table_ping_and_depth.py --input fq_RelocaTE2_Ping_NM2.Ping_copy.txt --depth rufipogon.bam.summary

echo "30 rufipogon Pong"
python Rice3k_copy_number_depth.py --input fq_RelocaTE2_Pong_NM2 --output fq_RelocaTE2_Pong_NM2.Pong_copy.txt &
python merge_table_ping_and_depth.py --input fq_RelocaTE2_Pong_NM2.Pong_copy.txt --depth rufipogon.bam.summary

echo "30 rufipogon mPing"
python Rice3k_copy_number_depth_mPing.py --input fq_RelocaTE2_mPing_NM2 --output fq_RelocaTE2_mPing_NM2.mPing_copy.txt &
python merge_table_ping_and_depth.py --input fq_RelocaTE2_mPing_NM2.mPing_copy.txt --depth rufipogon.bam.summary

#merge
paste fq_RelocaTE2_mPing_NM2.mPing_copy.depth.txt fq_RelocaTE2_Ping_NM2.Ping_copy.depth.txt fq_RelocaTE2_Pong_NM2.Pong_copy.depth.txt | cut -f1,3,7,11-12 > fq_RelocaTE2.mPing_Ping_Pong.copy.depth.txt

echo "50 rufipogon"
Rufipogon_50_RelocaTE2_Ping_NM2, Rufipogon_50.bam.summary
#Ping
python Rice3k_copy_number_depth.py --input Rufipogon_50_RelocaTE2_Ping_NM2 --output Rufipogon_50_RelocaTE2_Ping_NM2.Ping_copy.txt &
python merge_table_ping_and_depth.py --input Rufipogon_50_RelocaTE2_Ping_NM2.Ping_copy.txt --depth Rufipogon_50.bam.summary
#Pong
python Rice3k_copy_number_depth.py --input Rufipogon_50_RelocaTE2_Pong_NM2 --output Rufipogon_50_RelocaTE2_Pong_NM2.Pong_copy.txt &
python merge_table_ping_and_depth.py --input Rufipogon_50_RelocaTE2_Pong_NM2.Pong_copy.txt --depth Rufipogon_50.bam.summary
#mPing
python Rice3k_copy_number_depth_mPing.py --input Rufipogon_50_RelocaTE2_mPing_NM2 --output Rufipogon_50_RelocaTE2_mPing_NM2.mPing_copy.txt &
python merge_table_ping_and_depth.py --input Rufipogon_50_RelocaTE2_mPing_NM2.mPing_copy.txt --depth Rufipogon_50.bam.summary
#merge
paste Rufipogon_50_RelocaTE2_mPing_NM2.mPing_copy.depth.txt Rufipogon_50_RelocaTE2_Ping_NM2.Ping_copy.depth.txt Rufipogon_50_RelocaTE2_Pong_NM2.Pong_copy.depth.txt | cut -f1,3,7,11-12 > Rufipogon_50_RelocaTE2.mPing_Ping_Pong.copy.depth.txt

echo "57 rufipogon"
#Ping
python Rice3k_copy_number_depth.py --input Rufipogon_57_RelocaTE2_Ping_NM2 --output Rufipogon_57_RelocaTE2_Ping_NM2.Ping_copy.txt &
python merge_table_ping_and_depth.py --input Rufipogon_57_RelocaTE2_Ping_NM2.Ping_copy.txt --depth Rufipogon_57.bam.summary
#Pong
python Rice3k_copy_number_depth.py --input Rufipogon_57_RelocaTE2_Pong_NM2 --output Rufipogon_57_RelocaTE2_Pong_NM2.Pong_copy.txt &
python merge_table_ping_and_depth.py --input Rufipogon_57_RelocaTE2_Pong_NM2.Pong_copy.txt --depth Rufipogon_57.bam.summary
#mPing
python Rice3k_copy_number_depth_mPing.py --input Rufipogon_57_RelocaTE2_mPing_NM2 --output Rufipogon_57_RelocaTE2_mPing_NM2.mPing_copy.txt &
python merge_table_ping_and_depth.py --input Rufipogon_57_RelocaTE2_mPing_NM2.mPing_copy.txt --depth Rufipogon_57.bam.summary
#merge
paste Rufipogon_57_RelocaTE2_mPing_NM2.mPing_copy.depth.txt Rufipogon_57_RelocaTE2_Ping_NM2.Ping_copy.depth.txt Rufipogon_57_RelocaTE2_Pong_NM2.Pong_copy.depth.txt | cut -f1,3,7,11-12 > Rufipogon_57_RelocaTE2.mPing_Ping_Pong.copy.depth.txt

