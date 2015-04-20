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
from ete2 import Tree

def usage():
    test="name"
    message='''
python Draw_Nexus_Tree.py --input test.phy.nexus.newick --anno test.phy.anno --color 3 --trait 4 --showtips TRUE --output test.phy
python Draw_Nexus_Tree.py --input 3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree --anno rice_line_ALL_3000.anno.list --color 2 --trait 7 --subsample Japonica
python Draw_Nexus_Tree.py --input 3K_coreSNP-v2.1.binary.tab.landrace.nj.tree --anno rice_line_ALL_3000.anno.list --trait 7 --color 2 --sublist rice_line_ALL_3000.CAAS.list

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
--trait: colume to draw trait
--color: colume to draw color
--subsample: Japonica/Indica, if specified we sample only Japonica or Indica from tree and annotation file to draw tree
--sublist: file of list of subsample, if sepcified we sample only these taxa in list for tree and annotation file to draw tree
--subtitle: title for sublist files
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
                data[unit[0]] = 1
    return data


#B001    blue    Heibiao|B001|Temp       Heibiao China   Temperate japonica      60
def sub_list_anno(infile, sublist, sub_file):
    data = []
    sublist_dict = readtable(sublist)
    #r_1 = re.compile(r'_|-')
    ofile = open(sub_file, 'w')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if sublist_dict.has_key(unit[0]):
                    #unit[0] = re.sub(r'_', r'', unit[0])
                    line = '\t'.join(unit)
                    #unit[0] = '\'%s\'' %(unit[0]) if r_1.search(unit[0]) else unit[0]
                    #print unit[0]
                    data.append(unit[0])
                    ##make mPing with 0 to 1 just to check if data is empty
                    #if int(unit[6]) == 0:
                    #    unit[6] = '1'
                    #    line = '\t'.join(unit)
                    print >> ofile, line
                elif line.startswith(r'^Taxa'):
                    print >> ofile, line
    ofile.close()
    return data

#B001    blue    Heibiao|B001|Temp       Heibiao China   Temperate japonica      60
def sub_anno(infile, sample, sub_file):
    data = []
    r = re.compile(r'%s' %(sample), re.IGNORECASE)
    r_1 = re.compile(r'_|-')
    ofile = open(sub_file, 'w')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if r.search(unit[5]):
                    #unit[0] = re.sub(r'_', r'', unit[0])
                    line = '\t'.join(unit)
                    #unit[0] = '\'%s\'' %(unit[0]) if r_1.search(unit[0]) else unit[0]
                    #print unit[0]
                    data.append(unit[0])
                    ##make mPing with 0 to 1 just to check if data is empty
                    #if int(unit[6]) == 0:
                    #    unit[6] = '1'
                    #    line = '\t'.join(unit)
                    print >> ofile, line
                elif line.startswith(r'^Taxa'):
                    print >> ofile, line
    ofile.close()
    return data

def sub_tree_ape(intree, sub_anno, sub_tree, prefix):
    R_cmd='''
library("ape")
tree = read.tree(file="%s", )
anno = read.table(file="%s", sep='\\t')
retain_id = anno[,1]
pruned.tree = drop.tip(tree, tree$tip.label[-match(retain_id, tree$tip.label)])
write.tree(pruned.tree, file="%s")

#begin plot
tree = pruned.tree
x = read.table(file="3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree.Japonica.anno", sep='\t', header=1)
y = setNames(x[,7], x[,1])
y = y[match(gsub("'", '', tree$tip.label), names(y))]

sample_colors = setNames(x[,2], x[,1])
sample_colors = sample_colors[match(gsub("'", '', tree$tip.label), names(sample_colors))]
sample_colors = as.vector(sample_colors)

pdf("3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree.Japonica.pdf")
layout(matrix(c(1,2),1,2),c(0.7,0.3))
par(mar=c(4,1,2,2))
edge_colors=NULL

#https://ecomorph.wordpress.com/2014/10/09/phylogenetic-trees-in-r-4/
#edge_num includes all the edge of internal edge or termial edge.
#the latter is what we need.
edge_num = tree$edge[,2]
for (i in 1:length(edge_num)){
     if (edge_num[i] > length(sample_colors)){
         edge_colors[i] = 'black'
     }else{
         edge_colors[i] = sample_colors[edge_num[i]]
     }
}

plot(tree, edge.color=edge_colors, show.tip.label = FALSE)

barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 100, 200), line=1)
dev.off()
''' %(intree, sub_anno, sub_tree)

    ofile = open ('%s.subtree.R' %(prefix), 'w')
    print >> ofile, R_cmd
    ofile.close()
    os.system('cat %s.subtree.R | R --slave' %(prefix))

def sub_tree_ETE(intree, retain_ids, sub_tree):
    tree_t = Tree(intree, format=1)
    tree_t.prune(retain_ids)
    tree_t.write(format=1, outfile=sub_tree)

def sub_tree(intree, retain_ids, sub_tree):
    tree_t = dendropy.Tree()
    tree_t.read_from_path(intree, 'newick', preserve_underscores=True) 
    tree_t.retain_taxa_with_labels(retain_ids)
    tree_t.write_to_path(sub_tree, 'newick')

#tree_t = dendropy.Tree()
#tree_t.read_from_path(intree, 'newick')
#tree_t.write_to_path(outtree, 'nexus')


def write_R(newick, anno, col, color, prefix, tip):

    R_cmd='''
library("ape")
tree = read.tree(file="%s")
x = read.table(file="%s", sep='\\t', header=1)
y = setNames(x[,%s], x[,1])
y = y[match(gsub("'", '', tree$tip.label), names(y))]

pdf("%s.pdf")
layout(matrix(c(1,2),1,2),c(0.7,0.3))
par(mar=c(4,1,2,2))
plot(tree, show.tip.label = %s)
barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 100, 200), line=1)
dev.off()
''' %(newick, anno, col, prefix, tip)

    if int(color) > 0:
        R_cmd='''
library("ape")
tree = read.tree(file="%s")
x = read.table(file="%s", sep='\\t', header=1)
y = setNames(x[,%s], x[,1])
y = y[match(gsub("'", '', tree$tip.label), names(y))]

sample_colors = setNames(x[,%s], x[,1])
sample_colors = sample_colors[match(gsub("'", '', tree$tip.label), names(sample_colors))]
sample_colors = as.vector(sample_colors)

pdf("%s.pdf")
layout(matrix(c(1,2),1,2),c(0.7,0.3))
par(mar=c(4,1,2,4))
edge_colors=rep("black", length(tree$edge[,2]))

#https://ecomorph.wordpress.com/2014/10/09/phylogenetic-trees-in-r-4/
#edge_num includes all the edge of internal edge or termial edge.
#the latter is what we need.
edge_num = tree$edge[,2]
for (i in 1:length(edge_num)){
     if (edge_num[i] <= length(sample_colors)){
         if (!is.na(sample_colors[edge_num[i]])){
             edge_colors[i] = sample_colors[edge_num[i]]
         }
     }
}

plot(tree, edge.color=edge_colors, show.tip.label = %s)
leg_inf = cbind(as.vector(x[,2]), as.vector(x[,6]))
leg_inf = unique(leg_inf)
leg_inf = leg_inf[order(leg_inf[,2]),]
xrange  = par("xaxp")
yrange  = par("yaxp")
par(xpd=TRUE) #set this legend can be plot into margin area
#legend(x=xrange[2]*0.8, y=yrange[2]*0.99, substr(leg_inf[,2], 1, 4), fill=leg_inf[,1], border=FALSE, bty='n')
legend(x=xrange[2]*0.8, y=yrange[2]*0.99, leg_inf[,2], fill=leg_inf[,1], border=FALSE, bty='n')

par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 100, 200), line=1)
dev.off()
''' %(newick, anno, col, color, prefix, tip)

    ofile = open ('%s.R' %(prefix), 'w')
    print >> ofile, R_cmd
    ofile.close()
    os.system('cat %s.R | R --slave' %(prefix))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-a', '--anno')
    parser.add_argument('-c', '--color')
    parser.add_argument('-t', '--trait')
    parser.add_argument('-n', '--showtips')
    parser.add_argument('-s', '--subsample')
    parser.add_argument('--sublist')
    parser.add_argument('--subtitle')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        os.path.isfile(args.input) and os.path.isfile(args.anno)
    except:
        usage()
        sys.exit(2)

    if not args.color:
        args.color = 0
    if not args.showtips:
        args.showtips = 'FALSE'

    tree_file = args.input
    anno_file = args.anno
    color     = args.color
    colume    = args.trait
    prefix    = args.output
    sample    = args.subsample
    if args.subsample:
        #pass
        sub_tree_file = '%s.%s.tree' %(tree_file, sample)
        sub_anno_file = '%s.%s.anno' %(tree_file, sample)
        sub_prefix    = '%s.%s' %(tree_file, sample)
        retain_ids = sub_anno(anno_file, sample, sub_anno_file)
        sub_tree(tree_file, retain_ids, sub_tree_file)
        #sub_tree_ape(tree_file, sub_anno_file, sub_tree_file, sub_prefix)
        #sub_tree_ETE(tree_file, retain_ids, sub_tree_file)
        write_R(sub_tree_file, sub_anno_file, colume, color, sub_prefix, args.showtips)
    elif args.sublist:
        if not args.subtitle:
            args.subtitle = 'CAAS'
        sub_tree_file = '%s.%s.tree' %(tree_file, args.subtitle)
        sub_anno_file = '%s.%s.anno' %(tree_file, args.subtitle)
        sub_prefix    = '%s.%s' %(tree_file, args.subtitle)
        retain_ids = sub_list_anno(anno_file, args.sublist, sub_anno_file)
        sub_tree(tree_file, retain_ids, sub_tree_file)
        write_R(sub_tree_file, sub_anno_file, colume, color, sub_prefix, args.showtips)
    else:
        write_R(tree_file, anno_file, colume, color, prefix, args.showtips)    

if __name__ == '__main__':
    main()

