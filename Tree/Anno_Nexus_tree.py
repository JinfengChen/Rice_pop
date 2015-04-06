#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
import dendropy

def usage():
    test="name"
    message='''
python Anno_Nexus_tree.py --input test.phy.nexus.newick --format newick --anno test.phy.anno

Annotation tree file with color and other table information.
1. if the tree is newick not nexus we convert newick to nexus
2. Add annotation table into nexus tree, put color on branch and leaf if specified

--infile: input tree file
(Gamma:0.46568,(Beta:-0.15920,(Delta:0.12426,Epsilon:0.04163):0.84286):0.05225,Alpha:0.39186):0.00000;
--format: format of tree file (newick and nexus), default is nexus, optional
--anno: annotation table file, we only convert newick to nexus if anno table is not specified, optional
Taxa	Origin	Color
Gamma	indian	orange
Beta	china	yellow
Delta	UK	gray
Epsilon	EPS	blue
Alpha	US	red
--color: annotate color for branch or leaf or both, b/l/bl, optional

    '''
    print message


def readanno(infile):
    data = defaultdict(lambda : defaultdict(lambda : str()))
    header = []
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if unit[0] == 'Taxa':
                    header = unit
                    for i in range(len(header)):
                        if header[i] == 'Color' or header[i] == 'color':
                            header[i] = '!color'
                else:
                    for i in range(1, len(unit)):
                        data[unit[0]][header[i]] = unit[i]
    return data

def figtree_color():
    color = defaultdict(lambda : str())
    color = {
        'red'     : '#C13900',
        'orange'  : '#833F00',
        'gray'    : '#3F4353',
        'yellow'  : '#FF7C00',
        'blue'    : '#008BFF',
        'green'   : '#416214'
    }
    #for k in color.keys():
    #    print k, color[k]
    return color

def valid_nexus(intree):
    tree_t = dendropy.Tree()
    try:
        tree_t.write_to_path(outtree, 'nexus')
    except:
        sys.exit(2)

def newick2nexus(intree):
    outtree= '%s.nexus.tree' %(intree)
    tree_t = dendropy.Tree()
    tree_t.read_from_path(intree, 'newick')
    tree_t.write_to_path(outtree, 'nexus')
    return outtree

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-f', '--format')
    parser.add_argument('-a', '--anno')
    parser.add_argument('-c', '--color')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()

    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    #set color to branck or leaf
    if not args.color:
        args.color = 'bl'

    #get color table in figtree
    color_table = figtree_color()

    #valid tree format
    if not args.format:
        args.format = 'nexus'
        tree_t = dendropy.Tree()
        try:
            tree_t.read_from_path(args.input, 'nexus')
        except:
            print 'Not a nexus tree, Specify newick tree or nexus as input file and use --format newick if newick tree'
            sys.exit(2)

    #convert newick to nexus
    if args.format == 'newick':
        nexus_tree = newick2nexus(args.input)
        args.input = nexus_tree        

    rl = re.compile(r'l')
    rb = re.compile(r'b')
    #parse annotation and annoate nexus tree
    if args.anno:
        anno_tree = '%s.anno.tree' %(os.path.splitext(args.input)[0])
        anno = readanno(args.anno)
        #for taxa in sorted(anno.keys()):
        #    for key in anno[taxa].keys():
        #        print '%s\t%s\t%s' %(taxa, key, anno[taxa][key])
        tree = dendropy.Tree()
        tree.read_from_path(args.input, 'nexus')
        for taxon in tree.taxon_set:
            #print taxon, len(anno[str(taxon)].keys())
            taxa = str(taxon)
            for key in anno[taxa].keys():
                ##attr is not a variable but a string used for all attribute we assigned.
                ##key is a variable that we speficy name for each attribute we assigned
                ##alway assign value to taxon.attr first then add_bound_attribute after that
                if key == '!color':
                    if rl.search(args.color):
                        taxon.attr = color_table[anno[taxa][key]]
                        taxon.annotations.add_bound_attribute('attr', key)
                else:
                    taxon.attr = anno[taxa][key]
                    taxon.annotations.add_bound_attribute('attr', key)

        ##annotation branch
        for node in tree.postorder_node_iter():
            if node.taxon is not None:
                taxa = str(node.taxon)
                if anno[taxa].has_key('!color') and rb.search(args.color):
                    node.color = color_table[anno[taxa]['!color']]
                    node.annotations.add_bound_attribute('color', '!color')
                else:
                    pass
        tree.write_to_path(anno_tree, 'nexus')


if __name__ == '__main__':
    main()

