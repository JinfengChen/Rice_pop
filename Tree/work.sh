wget http://oryzasnp-atcg-irri-org.s3-website-ap-southeast-1.amazonaws.com/3krg-coresnp-v2.1/3K_coreSNP-v2.1.plink.tar.gz > log 2> log2 &
python plink2maf.py --input 3K_coreSNP-v2.1.ped
echo "tree"
qsub tree.sh
perl vcf_tab_to_fasta_alignmentv1.pl -i 3K_coreSNP-v2.1.pruneddata.tab > 3K_coreSNP-v2.1.pruneddata.tab.pos &
perl /rhome/cjinfeng/software/bin/fastaDeal.pl --attr id:len 3K_coreSNP-v2.1.pruneddata.tab.fasta > 3K_coreSNP-v2.1.pruneddata.tab.fasta.len &


echo "annotaion tree, ALL_3000"
python Anno_Nexus_tree.py --input 3K_coreSNP-v2.1.pruneddata.tab.fasttree.tree --format newick --anno ../GigaScience/rice_line_ALL_3000.anno.figtree.list --color bl
python Anno_Nexus_tree.py --input 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree --format newick --anno ../GigaScience/rice_line_ALL_3000.anno.figtree.list --color bl

echo "Draw tree with trait"
python Draw_Nexus_Tree.py --input 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree --anno rice_line_ALL_3000.anno.list --trait 7 --color 2 --output 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree
python Draw_Nexus_Tree.py --input 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree --anno rice_line_ALL_3000.anno.list --trait 7 --color 2 --subsample Japonica --output 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree

echo "rice 3000"

qsub -q js run_Build_tree.sh

echo "Anno tree"
python Anno_Nexus_tree.py --input 3K_coreSNP-v2.1.binary.tab.fasta.fasttree.nomle.nj.tree --format newick --anno rice_line_ALL_3000.anno.list --color bl
echo "Draw tree with trait"
python Draw_Nexus_Tree.py --input 3K_coreSNP-v2.1.binary.tab.fasta.fasttree.nomle.nj.tree --anno rice_line_ALL_3000.anno.list --trait 7 --color 2 --output 3K_coreSNP-v2.1.binary.tab.fasta.fasttree.nomle.nj.tree
