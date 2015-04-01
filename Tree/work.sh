wget http://oryzasnp-atcg-irri-org.s3-website-ap-southeast-1.amazonaws.com/3krg-coresnp-v2.1/3K_coreSNP-v2.1.plink.tar.gz > log 2> log2 &
python plink2maf.py --input 3K_coreSNP-v2.1.ped
echo "tree"
qsub tree.sh
