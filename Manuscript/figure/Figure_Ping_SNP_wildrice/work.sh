echo "test"
python Ping_SNP.py --input test_3k_Ping

echo "446 rufipgon 16th SNP"
python Ping_SNP.py --input Wildrice_fastq_RelocaTEi_Ping > log 2>&1 &

echo "30 rufipogon 16th SNP"
python Ping_SNP.py --input fq_RelocaTE2_Ping > log 2>&1 &

