echo "ping coverage"
python Rice3k_Ping_Coverage.py --input rice_line_ALL_3000.anno.list > log 2>&1 &
python Rice3k_Ping_Coverage_Actin.py --input rice_line_ALL_3000.anno.list --output actin_coverage_rice3000_MSU7.matrix > log 2>&1 &
python Rice3k_Ping_Coverage_Pong.py --input rice_line_ALL_3000.anno.list --output pong_coverage_rice3000_MSU7.matrix > log 2>&1 &
python Rice3k_Ping_Coverage_Control.py --input rice_line_ALL_3000.anno.list --output control_coverage_rice3000_MSU7.matrix > log 2>&1 &

echo "reorder by ping order"
python Ping_Coverage_matrix_ReOrder.py --ref ping_coverage_rice3000_MSU7.matrix.header --qry pong_coverage_rice3000_MSU7.matrix.header
python Ping_Coverage_matrix_ReOrder.py --ref ping_coverage_rice3000_MSU7.matrix.header --qry control_coverage_rice3000_MSU7.matrix.header
python Ping_Coverage_matrix_ReOrder.py --ref ping_coverage_rice3000_MSU7.matrix.header --qry actin_coverage_rice3000_MSU7.matrix.header
python Ping_Coverage_matrix_ReOrder.py --ref ping_coverage_rice3000_MSU7.matrix.header --qry rice_3k_depth.txt

echo "read depth"
python Rice3k_Ping_Coverage_Depth.py --input rice_line_ALL_3000.anno.list > log 2>&1 &
python Rice3k_Ping_Coverage_Depth_unfinished.py --input rice_line_ALL_3000.anno.list > log 2>&1 &

echo "get results when still running"
python Rice3k_Ping_Coverage_tempmatrix.py --input rice_line_ALL_3000.anno.list > log 2>&1 &
python Rice3k_Ping_Coverage_ID_info.py --input ping_coverage_rice3000_MSU7.matrix.header > ping_coverage_rice3000_MSU7.matrix.id_info &
python Ping_Coverage_matrix_unfinished.py --input ping_coverage_3k
python Ping_Coverage_matrix_finished_gz.py --input ping_coverage_3k
python Rice3k_Ping_Coverage_download_bam.py --input rice_line_ALL_3000.anno.list
python Rice3k_Ping_Coverage_download_bam_Ping.py --input rice_line_ALL_3000.anno.list
python Rice3k_Ping_Coverage_download_bam_Pong.py --input rice_line_ALL_3000.anno.list
python Rice3k_Ping_Coverage_download_bam_Control.py --input rice_line_ALL_3000.anno.list
python Rice3k_Ping_Coverage_download_bam_Actin.py --input rice_line_ALL_3000.anno.list

awk '$2<1000' actin_coverage_rice3000_MSU7.matrix.header | cut -f1 | sed 's/.actin.coverage.clean.txt//' | sort > actin.empty

echo "rice strains may have intact Ping: 5339"
python Summary_Ping_Pong_intact.py --input ping_coverage_rice3000_MSU7.matrix.header
#228 intact, 7.6%=228/3000, ping and actin both > 70% coverage
awk '$3>=0.7 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | wc -l
#146 truncated, ping >=0.3 and ping < 0.7 and actin > 0.7
awk '$3<0.7 && $3>=0.3 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | wc -l
#truncated classification
awk '$3<0.7 && $3>=0.3 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | cut -f5 | grep "Indica" -c
awk '$3<0.7 && $3>=0.3 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | cut -f5 | grep "Temperate" -c
awk '$3<0.7 && $3>=0.3 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | cut -f5 | grep "Tropical" -c
awk '$3<0.7 && $3>=0.3 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | cut -f5 | grep "Intermediate" -c
awk '$3<0.7 && $3>=0.3 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | cut -f5 | grep "boro" -c
awk '$3<0.7 && $3>=0.3 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | cut -f5 | grep "Basmati" -c
#all rice
cat rice_line_ALL_3000.anno.list | grep "Indica" -c
cat rice_line_ALL_3000.anno.list | grep "Temperate" -c
cat rice_line_ALL_3000.anno.list | grep "Tropical" -c
cat rice_line_ALL_3000.anno.list | grep "Intermediate" -c
cat rice_line_ALL_3000.anno.list | grep "boro" -c
cat rice_line_ALL_3000.anno.list | grep "Basmati" -c
#intact 
awk '$3>=0.7 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | grep "Indica" -c
awk '$3>=0.7 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | grep "Temperate" -c
awk '$3>=0.7 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | grep "Tropical" -c
awk '$3>=0.7 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | grep "Intermediate" -c
awk '$3>=0.7 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | grep "boro" -c
awk '$3>=0.7 && $4>=0.7' ping_coverage_rice3000_MSU7.matrix.header.sum | grep "Basmati" -c



echo "rice strains may have intact Pong: 5164"
#70% of Pong coverage, 3614=5164*0.7


