
python make_target_nonauto_general_redo.py `pwd`/query/ `pwd`/Target `pwd`/reference/MSU7.fa Target_Run_MITE_MSU7


sort -k8,8rn Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.txt | awk '$6>200' | grep "rice_3_41532"
sort -k8,8rn Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.txt | awk '$6>200' | grep "rice_2_73170"
sort -k8,8rn Target/Target_Run_MITE_MSU7_2017_03_15_143604.MITE_copy_identify.txt | awk '$6>200' | grep "rice_1_128219

