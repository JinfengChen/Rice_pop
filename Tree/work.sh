wget http://oryzasnp-atcg-irri-org.s3-website-ap-southeast-1.amazonaws.com/3krg-coresnp-v2.1/3K_coreSNP-v2.1.plink.tar.gz > log 2> log2 &
python plink2maf.py --input 3K_coreSNP-v2.1.ped
echo "tree"
qsub tree.sh
perl vcf_tab_to_fasta_alignmentv1.pl -i 3K_coreSNP-v2.1.pruneddata.tab > 3K_coreSNP-v2.1.pruneddata.tab.pos &
perl /rhome/cjinfeng/software/bin/fastaDeal.pl --attr id:len 3K_coreSNP-v2.1.pruneddata.tab.fasta > 3K_coreSNP-v2.1.pruneddata.tab.fasta.len &


echo "annotaion tree, ALL_3000"
python Anno_Nexus_tree.py --input 3K_coreSNP-v2.1.pruneddata.tab.fasttree.tree --format newick --anno ../GigaScience/rice_line_ALL_3000.anno.list --color bl
python Anno_Nexus_tree.py --input 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree --format newick --anno ../GigaScience/rice_line_ALL_3000.anno.list --color bl

