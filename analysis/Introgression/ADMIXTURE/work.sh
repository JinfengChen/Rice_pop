sbatch --array 2-15 run_ADMIXTURE.sh
cat multi_run.R | R --slave
python Summary_Cluster.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.8.Q
python Summary_Cluster_3k_pop.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.8.Q

echo "tree tip"
cat 3K_coreSNP-v2.1.binary.tab.landrace.nj.landrace.tree_mPing_Ping_Pong.strain_list.R | R --slave
echo "reorder Q matrix using tree tip"
python Reorder_Q.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.8.Q --reorder_list 3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.tip.label.txt
python Reorder_Q.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.14.Q --reorder_list 3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.tip.label.txt

echo "sorted by Q8"
paste core_v0.7.pruneddata3.structure.nosex core_v0.7.pruneddata3.8.Q | cut -f2- | sort -k5,5nr -k4,4nr -k8,8nr -k1,1nr -k7,7nr -k6,6nr -k2,2nr -k3,3nr > core_v0.7.pruneddata3.8.Q.strains_order.list
python Reorder_Q.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.8.Q --reorder_list core_v0.7.pruneddata3.8.Q.strains_order.list
sbatch --array 2-15 run_ADMIXTURE_reorder.sh
#new sort
python Sort_ClusterQ8.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.8.Q | sort -k2,2nr -k4,4n -k5,5n > core_v0.7.pruneddata3.8.Q.sorted.txt
python Reorder_Q.py --strain_list core_v0.7.pruneddata3.structure.nosex --meanQ_list core_v0.7.pruneddata3.8.Q --reorder_list core_v0.7.pruneddata3.8.Q.sorted.txt
cat single_run_colored_defined.R | R --slave
sbatch --array 2-15 run_ADMIXTURE_reorder.sh

echo "plot"
#rainbow color
cat multi_run_raw.R | R --slave
#defined Q8 color
cat multi_run_color_defined.R | R --slave

echo "add barplot into 3k tree"
cp ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure2_3000_rice_tree/3K_coreSNP-v2.1.binary.tab.landrace.nj.landrace.tree_mPing_Ping_Pong.R ./
cp ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure2_3000_rice_tree/rice_line_ALL_3000.anno.landrace.list ./
cp ~/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure2_3000_rice_tree/3K_coreSNP-v2.1.binary.tab.landrace.nj.tree ./

echo "compare 3k new pop with old pop assignment"
python Compare_Pop_Assign.py --strain_list core_v0.7.pruneddata3.structure.nosex > 3k_pop.compare_with_old.txt
echo "Japonica high Ping strains"
awk -F"\t" '$8>1' rice_line_ALL_3000.anno.list | grep "Japonica" > rice_line_ALL_3000.anno.list.Japonica_2.list
python sum_pop_distri_general.py --input rice_line_ALL_3000.anno.list.Japonica_2.list
python sum_pop_distri_general_3k_pop.py --input rice_line_ALL_3000.anno.list.Japonica_2.list
