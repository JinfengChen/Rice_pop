#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
import pylab

def usage():
    test="name"
    message='''
python Draw_Nexus_Tree.py --input figtree/test.phy.nexus.newick --anno figtree/test.phy.anno

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

def write_R(newick, anno, output):

    R_cmd='''
library("ape")
tree = read.tree(file="%s")
x = read.table(file="%s", header=1)
y = setNames(x[,4], x[,1])

pdf("test.pdf")
layout(matrix(c(1,2),1,2),c(0.7,0.3))
#par(mfrow=c(1,2))
#par(mar=c(4.1,0,1.1,1.1))
#plotTree(tree, mar=c(5.1,2,1.1,1.1))
plot(tree,edge.color=c('red','green','red','gray','orange'))
par(mar=c(5.1,2,1.1,1.1))
barplot(y,horiz=TRUE,width=1,space=0, ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0,20,40), line=3)
dev.off()
''' %(newick, anno)
    ofile = open (output, 'w')
    print >> ofile, R_cmd
    ofile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-a', '--anno')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        os.path.isfile(args.input) and os.path.isfile(args.anno)
    except:
        usage()
        sys.exit(2)

    tree_file = args.input
    anno_file = args.anno
    write_R(tree_file, anno_file, 'tree_trait.R')    

if __name__ == '__main__':
    main()

