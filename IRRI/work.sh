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

echo "other japonica strain from IRRI, N=694, other=667, highmping=27, 2 not jap"
python ReNameSRA_subset_others.py --input temperate.mPing.group.id
#do 0-6 for these cmd
python ReNameSRA_down.py --output Japonica_fastq > log 2> log2 &
python ReNameSRA_merge.py --input Japonica_fastq > log 2> log2 &
python ReNameSRA_merge_clean.py --input ./Japonica_fastq
bash clean.sh
python ReNameSRA_RelocaTEi.py --input Japonica_fastq > log 2> log2 &
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi --list ../GigaScience/rice_line_IRRI_2466.download.list > Japonica_fastq_RelocaTEi_otherJap_mPing.summary
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi --list ../GigaScience/rice_line_IRRI_2466.download.list > Japonica_fastq_RelocaTEi_otherJap_mPing01.summary
python newcall.py Japonica_fastq_RelocaTEi_otherJap_mPing01.summary Japonica_fastq_RelocaTEi_otherJap_mPing0.summary > Japonica_fastq_RelocaTEi_otherJap_mPing1.summary
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi --list ../GigaScience/rice_line_IRRI_2466.download.list > Japonica_fastq_RelocaTEi_otherJap_mPing012.summary &
python newcall.py Japonica_fastq_RelocaTEi_otherJap_mPing012.summary Japonica_fastq_RelocaTEi_otherJap_mPing01.summary > Japonica_fastq_RelocaTEi_otherJap_mPing2.summary
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi --list ../GigaScience/rice_line_IRRI_2466.download.list > Japonica_fastq_RelocaTEi_otherJap_mPing0123.summary &
python newcall.py Japonica_fastq_RelocaTEi_otherJap_mPing0123.summary Japonica_fastq_RelocaTEi_otherJap_mPing012.summary > Japonica_fastq_RelocaTEi_otherJap_mPing3.summary

echo "all IRRI jap"
cat Japonica_fastq_RelocaTEi_mPing.summary Japonica_fastq_RelocaTEi_otherJap_mPing0123.summary > Japonica_fastq_RelocaTEi_mPing_IRRI_Jap.summary
python ReNameSRA_sumcall.py --input Japonica_fastq_RelocaTEi_mPing --list ../GigaScience/rice_line_IRRI_2466.download.list > Japonica_fastq_RelocaTEi_mPing_IRRI_Jap.summary

echo "Download Non japonica strains"
python ReNameSRA_subset_others_pop.py
python ReNameSRA_down.py --output Other_fastq > log 2> log2 &
python ReNameSRA_merge.py --input Other_fastq > log 2> log2 &
python ReNameSRA_merge_clean.py --input ./Other_fastq
bash clean.sh
python ReNameSRA_RelocaTEi.py --input Other_fastq > log 2> log2 &
python ReNameSRA_sumcall.py --input Other_fastq_RelocaTEi --list ../GigaScience/rice_line_IRRI_2466.download.list
python ReNameSRA_sumcall.py --input Transposon_mPing_Ping_Pong/Other_fastq_RelocaTEi_mPing --list ../GigaScience/rice_line_IRRI_2466.download.list > Transposon_mPing_Ping_Pong/Other_fastq_RelocaTEi_mPing.summary

echo "summary call"
cat Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_mPing.summary Transposon_mPing_Ping_Pong/Other_fastq_RelocaTEi_mPing.summary > Transposon_mPing.IRRI.summary

echo "HEG4 related groups japonica"
python ReNameSRA_subset.py --input HEG4_close_group.list
mv HEG4_close_group.list.download.list rice_line_IRRI_2466.download.HEG4_group.list
cut -f1 ~/Rice/Rice_population_sequence/Rice_3000/Tree/3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.landrace_group.anno | grep "IRIS" | sed 's/\_//' | awk '{print $1"\t"$1}' > HEG4_temperate_group.list
python ReNameSRA_subset.py --input HEG4_temperate_group.list
mv HEG4_temperate_group.list.download.list rice_line_IRRI_2466.download.HEG4_temperate.list
python ReNameSRA_down.py --output HEG4_group > log 2>&1 &
python ReNameSRA_merge.py --input HEG4_group > log 2>&1 &
python ReNameSRA_merge_clean.py --input HEG4_group > log 2>&1 &
bash clean.sh
python ReNameSRA_RelocaTEi.py --input HEG4_group > log 2>&1 &
ls `pwd`/HEG4_group/ERS*/ERR*_1.fastq.gz | sed 's/_1/_?/' > HEG4_temperate_group.fastq.list
qsub fastq_stat.sh
echo "strain difference of TE"
python Strain_Diff.py --input HEG4_group_RelocaTEi > HEG4_group_RelocaTEi.TEdiff 

echo "call mPing/Ping/Ping and other TE for all IRRI strain"
#Japonica
python ReNameSRA_down.py --output Japonica_fastq > log 2>&1 &
python ReNameSRA_merge.py --input Japonica_fastq > log 2>&1 &
python ReNameSRA_merge_clean.py --input Japonica_fastq > log 2>&1 &
python ReNameSRA_RelocaTEi_mPing.py --input Japonica_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/mping.fa > log 2>&1
python ReNameSRA_RelocaTEi_mPing.py --input Japonica_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa > log 2>&1
python ReNameSRA_RelocaTEi_mPing.py --input Japonica_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/pong.fa > log 2>&1
python ReNameSRA_RelocaTEi.py --input Japonica_fastq > log 2>&1 &
python ReNameSRA_sum_unfinished.py --input Japonica_fastq_RelocaTEi
#other rice
python ReNameSRA_down.py --output Other_fastq > log 2>&1 &
python ReNameSRA_merge.py --input Other_fastq > log 2>&1 &
python ReNameSRA_merge_clean.py --input Other_fastq > log 2>&1 &
python ReNameSRA_RelocaTEi_mPing.py --input Other_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/mping.fa > log 2>&1
python ReNameSRA_RelocaTEi_mPing.py --input Other_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa > log 2>&1
python ReNameSRA_RelocaTEi_mPing.py --input Other_fastq --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/pong.fa > log 2>&1
python ReNameSRA_RelocaTEi.py --input Other_fastq > log 2>&1 &
python ReNameSRA_sum_unfinished.py --input Other_fastq_RelocaTEi

#other, quick run
python ReNameSRA_down.py --output Other_fastq_S > log 2>&1 &
python ReNameSRA_merge.py --input Other_fastq_S > log 2>&1 &
python ReNameSRA_merge_clean.py --input Other_fastq_S > log 2>&1 &
python ReNameSRA_RelocaTEi_mPing.py --input Other_fastq_S --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/mping.fa > log 2>&1
python ReNameSRA_RelocaTEi_mPing.py --input Other_fastq_S --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa > log 2>&1
python ReNameSRA_RelocaTEi_mPing.py --input Other_fastq_S --repeat /rhome/cjinfeng/BigData/00.RD/RelocaTE_i/Simulation/Reference/pong.fa > log 2>&1
python ReNameSRA_RelocaTEi.py --input Other_fastq_S > log 2>&1 &
python ReNameSRA_sum_unfinished.py --input Other_fastq_S_RelocaTEi


echo "strain number in japonica and others: 2466=694jap+1772other"
cut -f5 rice_line_IRRI_2466.Japonica.download.list | uniq | sort | uniq | wc -l
#694
cut -f5 rice_line_IRRI_2466.other.download.list | uniq | sort | uniq | wc -l
#other strain=1772
echo "clean japonica results"
python Clean_Japonica_RelocaTEi.py --input Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_Ping/
python Clean_Japonica_RelocaTEi.py --input Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_mPing/
python Clean_Japonica_RelocaTEi.py --input Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_Pong/

echo "summary ping"
python ReNameSRA_sum_Ping.py --input Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_Ping --list rice_line_IRRI_2466.download.list
python ReNameSRA_sum_Pong.py --input Transposon_mPing_Ping_Pong/Japonica_fastq_RelocaTEi_Pong --list rice_line_IRRI_2466.download.list

