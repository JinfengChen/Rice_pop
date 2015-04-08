#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
import pylab
import dendropy

def usage():
    test="name"
    message='''
python Draw_Nexus_Tree.py --input test.phy.nexus.newick --anno test.phy.anno --col 4 --output test.phy
python Draw_Nexus_Tree.py --input 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree --anno rice_line_ALL_3000.anno.list --col 7 --subsample Japonica --output 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree

Plot newick phylogenetic tree with trait values in barplot using phytools in R.
http://blog.phytools.org/2014/05/new-version-of-plottreewbars-that.html
http://blog.phytools.org/2014/10/colors-terminal-edges-in-plottreewbars.html

--infile: input tree file
(Gamma:0.46568,(Beta:-0.15920,(Delta:0.12426,Epsilon:0.04163):0.84286):0.05225,Alpha:0.39186):0.00000;
--anno: annotation table file, we only convert newick to nexus if anno table is not specified, optional
Taxa	Origin	Color
Gamma	indian	orange
Beta	china	yellow
Delta	UK	gray
Epsilon	EPS	blue
Alpha	US	red
--col: columen to draw trait
--subsample: Japonica/Indica, if specified we sample only Japonica or Indica from tree and annotation file to draw tree
--output: output prefix of R and pdf
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def readtable(infile):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if not data.has_key(unit[0]):
                    data[unit[0]] = unit[1]
    return data


#B001    blue    Heibiao|B001|Temp       Heibiao China   Temperate japonica      60
def sub_anno(infile, sample, sub_file):
    data = []
    r = re.compile(r'%s' %(sample), re.IGNORECASE)
    ofile = open(sub_file, 'w')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if r.search(unit[5]):
                    unit[0] = re.sub(r'_', r'', unit[0])
                    line = '\t'.join(unit)
                    data.append(unit[0])
                    ##make mPing with 0 to 1 just to check if data is empty
                    #if int(unit[6]) == 0:
                    #    unit[6] = '1'
                    #    line = '\t'.join(unit)
                    print >> ofile, line
    ofile.close()
    return data


def sub_tree(intree, retain_ids, sub_tree):
    tree_t = dendropy.Tree()
    tree_t.read_from_path(intree, 'newick') 
    tree_t.retain_taxa_with_labels(retain_ids)
    tree_t.write_to_path(sub_tree, 'newick')

#tree_t = dendropy.Tree()
#tree_t.read_from_path(intree, 'newick')
#tree_t.write_to_path(outtree, 'nexus')


def write_R(newick, anno, col, prefix):

    R_cmd='''
library("ape")
tree = read.tree(file="%s")
x = read.table(file="%s", sep='\\t', header=1)
y = setNames(x[,%s], x[,1])
y = y[match(gsub("'", '', tree$tip.label), names(y))]

pdf("%s.pdf")
layout(matrix(c(1,2),1,2),c(0.7,0.3))
#par(mfrow=c(1,2))
#par(mar=c(4.1,0,1.1,1.1))
par(mar=c(4,1,2,2))
#plotTree(tree, mar=c(5.1,2,1.1,1.1))
#plot(tree,edge.color=c('red','green','red','gray','orange'))
plot(tree, show.tip.label = FALSE)
#plot(tree)
#par(mar=c(5.1,2,1.1,1.1))
barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 100, 200), line=1)
dev.off()
''' %(newick, anno, col, prefix)
    ofile = open ('%s.R' %(prefix), 'w')
    print >> ofile, R_cmd
    ofile.close()
    os.system('cat %s.R | R --slave' %(prefix))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-a', '--anno')
    parser.add_argument('-c', '--col')
    parser.add_argument('-s', '--subsample')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        os.path.isfile(args.input) and os.path.isfile(args.anno)
    except:
        usage()
        sys.exit(2)


    tree_file = args.input
    anno_file = args.anno
    colume    = args.col
    prefix    = args.output
    sample    = args.subsample
    if args.subsample:
        #pass
        sub_tree_file = '%s.%s.tree' %(tree_file, sample)
        sub_anno_file = '%s.%s.anno' %(tree_file, sample)
        sub_prefix    = '%s.%s' %(tree_file, sample)
        retain_ids = sub_anno(anno_file, sample, sub_anno_file)
        sub_tree(tree_file, retain_ids, sub_tree_file)
        write_R(sub_tree_file, sub_anno_file, colume, sub_prefix)
    else:
        write_R(tree_file, anno_file, colume, prefix)    

if __name__ == '__main__':
    main()

