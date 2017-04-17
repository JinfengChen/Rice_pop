echo "test"
python Ping_SNP.py --input test_3k_Ping

echo "446 rufipgon 16th SNP"
python Ping_SNP.py --input Wildrice_fastq_RelocaTEi_Ping > log 2>&1 &

echo "30 rufipogon 16th SNP"
python Ping_SNP.py --input fq_RelocaTE2_Ping > log 2>&1 &

echo "50 rufipogon 16th SNP"
python Ping_SNP.py --input Rufipogon_50_RelocaTE2_Ping > log 2>&1 &
python Pong_SNP.py --input Rufipogon_50_RelocaTE2_Pong > log 2>&1 &
python mPing_SNP.py --input Rufipogon_50_RelocaTE2_mPing > log 2>&1 &
#map read by PE
python Ping_SNP_PE.py --input Rufipogon_50_RelocaTE2_Ping > log 2>&1 &

echo "57 rufipogon 16th SNP"
python Ping_SNP.py --input Rufipogon_57_RelocaTE2_Ping > log 2>&1 &
python Pong_SNP.py --input Rufipogon_57_RelocaTE2_Pong > log 2>&1 &
python mPing_SNP.py --input Rufipogon_57_RelocaTE2_mPing > log 2>&1 &
#map read by PE
python Ping_SNP_PE.py --input Rufipogon_57_RelocaTE2_Ping > log 2>&1 &


