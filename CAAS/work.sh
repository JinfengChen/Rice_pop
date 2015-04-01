echo "download"
python ReNameSRA_down.py > log 2> log2 &

echo "dump to fastq and gunzip fastq"
python ReNameSRA_merge_subset.py --input ./CAAS_1 > log 2> log2 &

echo "clean sra directory that finished sra2fastq convertion"
python ReNameSRA_merge_clean.py --input ./CAAS_1
bash clean.sh

echo "run RelocaTEi"
python ReNameSRA_RelocaTEi.py --input Japonica_fastq > log 2> log2 &
python ReNameSRA_RelocaTEi.py --input Japonica_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/pong.fa > log 2> log2 &

echo "summary"
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi_mPing --list rice_line_CAAS_534.download.list > Japonica_fastq_RelocaTEi_mPing.summary
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi_Pong --list rice_line_CAAS_534.download.list > Japonica_fastq_RelocaTEi_Pong.summary

