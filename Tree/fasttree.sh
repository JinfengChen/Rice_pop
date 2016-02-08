#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=10gb
#PBS -l walltime=100:00:00
#PBS -V

cd $PBS_O_WORKDIR

#module load treebest
#treebest nj example.maf > example.nhx
#treebest nj test.fasta > test.nhx
#/rhome/cjinfeng/software/tools/fasttree/FastTree -nt test.fasta > test.fasttree.tree
#/rhome/cjinfeng/software/tools/fasttree/FastTree -nt 3K_coreSNP-v2.1.pruneddata.tab.fasta > 3K_coreSNP-v2.1.pruneddata.tab.fasttree.tree
#/rhome/cjinfeng/software/tools/fasttree/FastTree -noml -nome -nt 3K_coreSNP-v2.1.pruneddata.tab.fasta > 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree
#/rhome/cjinfeng/software/tools/fasttree/FastTree -noml -nome -nt 3K_coreSNP-v2.1.binary.tab.fasta > 3K_coreSNP-v2.1.binary.tab.fasta.fasttree.nomle.nj.tree
#/rhome/cjinfeng/software/tools/fasttree/FastTree -nt 3K_coreSNP-v2.1.binary.tab.fasta > 3K_coreSNP-v2.1.binary.tab.fasta.fasttree.nj.tree
/rhome/cjinfeng/software/tools/fasttree/FastTree -noml -nome -nt 3K_coreSNP-v2.1.binary.tab.landrace.fasta > 3K_coreSNP-v2.1.binary.tab.landrace.nj.tree 

echo "Done"
