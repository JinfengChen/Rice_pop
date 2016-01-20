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


echo "other strain, not japonica"
python ReNameSRA_subset_others.py
python ReNameSRA_down.py --output Other_fastq > log 2> log2 &
python ReNameSRA_merge.py --input Other_fastq > log 2> log2 &
python ReNameSRA_merge_clean.py --input ./Other_fastq
bash clean.sh
python ReNameSRA_RelocaTEi.py --input Other_fastq > log 2> log2 &
python ReNameSRA_sumcall.py --input Other_fastq_RelocaTEi --list ../GigaScience/rice_line_CAAS_534.download.list > Other_fastq_RelocaTEi_other_mPing0.summary
python ReNameSRA_RelocaTEi.py --input Other_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/pong.fa > log 2> log2 &
python ReNameSRA_RelocaTEi.py --input Other_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa > log 2> log2 &

echo "redo unfinished, some do not have mPing/Ping/Pong, so no results directory. check flanking_seq directory first when you have list"
python ReNameSRA_sumcall.py --input Other_fastq_RelocaTEi_mPing --list ../GigaScience/rice_line_CAAS_534.download.list --check 1
python ReNameSRA_redo.py --input redo.list
python ReNameSRA_down.py --output Other_fastq1 > log 2> log2 &
python ReNameSRA_merge.py --input Other_fastq1 > log 2> log2 &
python ReNameSRA_merge_clean.py --input ./Other_fastq1
bash clean.sh
python ReNameSRA_RelocaTEi.py --input Other_fastq > log 2> log2 &

python ReNameSRA_redo.py --input redo.list
python ReNameSRA_down.py --output Japonica_fastq > log 2> log2 &
python ReNameSRA_merge.py --input Japonica_fastq > log 2> log2 &
python ReNameSRA_merge_clean.py --input ./Japonica_fastq
bash clean.sh
python ReNameSRA_RelocaTEi.py --input Japonica_fastq > log 2> log2 &

echo "summary, ping and pong not right because of similarity"
python ReNameSRA_sumcall.py --input Other_fastq_RelocaTEi_mPing --list ../GigaScience/rice_line_CAAS_534.download.list > Other_fastq_RelocaTEi_mPing.summary
python ReNameSRA_sumcall.py --input Other_fastq_RelocaTEi_Ping --list ../GigaScience/rice_line_CAAS_534.download.list > Other_fastq_RelocaTEi_Ping.summary
python ReNameSRA_sumcall.py --input Other_fastq_RelocaTEi_Pong --list ../GigaScience/rice_line_CAAS_534.download.list > Other_fastq_RelocaTEi_Pong.summary

echo "summary call"
cat Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_mPing.summary Transposon_mPing_Ping_Pong/Other_fastq_RelocaTEi_mPing.summary > Transposon_mPing.CAAS.summary


echo "use RelocaTE2_mPing to call Ping and Pick_Ping.py to generate Ping.gff"
python ReNameSRA_down.py --output Japonica_fastq > log 2> log2 &
python ReNameSRA_merge.py --input Japonica_fastq > log 2> log2 &
python ReNameSRA_merge_clean.py --input ./Japonica_fastq
bash clean.sh
python ReNameSRA_RelocaTEi_mPing.py --input Japonica_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa > log 2>&1
#sum ping, mping and pong, need to finish mping and pong
#ping
python ReNameSRA_sum_Ping.py --input Transposon_mPing_Ping_Pong_relocate/Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_Ping --list ../GigaScience/rice_line_CAAS_534.download.list
python ReNameSRA_sum_Ping.py --input Transposon_mPing_Ping_Pong_relocate/Transposon_mPing_Ping_Pong/Other_fastq_RelocaTEi_Ping --list ../GigaScience/rice_line_CAAS_534.download.list
cat Transposon_mPing_Ping_Pong_relocate/Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_Ping.summary Transposon_mPing_Ping_Pong_relocate/Transposon_mPing_Ping_Pong/Other_fastq_RelocaTEi_Ping.summary | sort > Transposon_mPing_Ping_Pong.summary.jinfeng
paste Transposon_mPing_Ping_Pong.summary.jinfeng Transposon_mPing_Ping_Pong.summary.lulu | cut -f1,2,8,15 | wc -l
#pong
python ReNameSRA_sum_Pong.py --input Transposon_mPing_Ping_Pong_relocate/Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_Pong --list ../GigaScience/rice_line_CAAS_534.download.list
python ReNameSRA_sum_Pong.py --input Transposon_mPing_Ping_Pong_relocate/Transposon_mPing_Ping_Pong/Other_fastq_RelocaTEi_Pong --list ../GigaScience/rice_line_CAAS_534.download.list

#testing ping
python ReNameSRA_RelocaTEi_mPing.py --input Other_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa > log 2>&1 &

echo "use RelocaTE2 to call other ~3000 TE"
python ReNameSRA_RelocaTEi_OtherTE.py --input Japonica_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/Rice.TE.short.unique.fa > log 2>&1 
 
