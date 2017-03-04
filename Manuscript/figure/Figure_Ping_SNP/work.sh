echo "30 rufipogon 16th SNP"
python Ping_SNP.py --input fq_RelocaTE2 > log 2>&1 &

echo "446 rufipgon 16th SNP"
python Ping_SNP.py --input Wildrice_fastq_RelocaTEi_Ping > log 2>&1 &

echo "3000 rice 16th SNP"
python Ping_SNP.py --input Rice3k_3000_RelocaTEi_Ping > log 2>&1 &


