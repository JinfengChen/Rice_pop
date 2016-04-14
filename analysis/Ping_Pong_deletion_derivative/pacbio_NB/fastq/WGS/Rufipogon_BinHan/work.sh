echo "Ping"
python Ping_Coverage_matrix_MSU7.py --input bam --output ping_coverage_rufipogon400_MSU7.matrix.1 > log 2>&1 &

echo "pong"
python Ping_Coverage_matrix_MSU7_Pong.py --input bam --output pong_coverage_rufipogon400_MSU7.matrix.1 > log 2>&1 &

echo "control"
python Ping_Coverage_matrix_MSU7_Control.py --input bam --output control_coverage_rufipogon400_MSU7.matrix.1 > log 2>&1 &

echo "actin"
python Ping_Coverage_matrix_MSU7_Actin.py --input bam --output actin_coverage_rufipogon400_MSU7.matrix.1 > log 2>&1 &

echo "sample depth"
awk '{print $1"\t"$4}' ~/Rice/Rice_population_sequence/Rice_BinHan/Wildrice/Wildrice_bam.summary | grep "ERR" > Rufipogon.depth.txt

echo "reorder pong and control, actin"
python Ping_Coverage_matrix_ReOrder.py --ref ping_coverage_rufipogon400_MSU7.matrix.1.header --qry pong_coverage_rufipogon400_MSU7.matrix.1.header &
python Ping_Coverage_matrix_ReOrder.py --ref ping_coverage_rufipogon400_MSU7.matrix.1.header --qry control_coverage_rufipogon400_MSU7.matrix.1.header &

python Ping_Coverage_matrix_ReOrder.py --ref ping_coverage_rufipogon400_MSU7.matrix.1.header --qry Rufipogon.depth.txt
