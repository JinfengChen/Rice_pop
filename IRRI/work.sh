echo "shuiyuan300li group rice from rice_3000 website"
temperate.mPing.group
cut -f2 temperate.mPing.group | grep -v "B" | grep -v "ID" | sed 's/ //' > temperate.mPing.group.id

echo "download list"
python ReNameSRA_subset.py --input temperate.mPing.group.id
python ReNameSRA_down.py --output Japonica_fastq
python ReNameSRA_merge.py --input Japonica_fastq > log 2> log2 &

echo "call mPing"
python ReNameSRA_RelocaTEi.py --input Japonica_fastq > log 2> log2 &
python ReNameSRA_RelocaTEi.py --input Japonica_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/pong.fa > log 2> log2 &

echo "summary"
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi_mPing --list ../GigaScience/rice_line_IRRI_2466.download.list > Japonica_fastq_RelocaTEi_mPing.summary
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi_Pong --list ../GigaScience/rice_line_IRRI_2466.download.list > Japonica_fastq_RelocaTEi_Pong.summary

echo "other japonica strain from IRRI, N=694"
python ReNameSRA_subset_others.py --input temperate.mPing.group.id
#do 0-6 for these cmd
python ReNameSRA_down.py --output Japonica_fastq
python ReNameSRA_merge.py --input Japonica_fastq > log 2> log2 &
python ReNameSRA_merge_clean.py --input ./Japonica_fastq
bash clean.sh
python ReNameSRA_RelocaTEi.py --input Japonica_fastq > log 2> log2 &

