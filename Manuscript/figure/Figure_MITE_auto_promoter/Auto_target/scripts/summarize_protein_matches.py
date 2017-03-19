#!/usr/bin/env python


import sys
import os
import os.path
import fastaIO
from collections import defaultdict

args = sys.argv[1:]

def usage():
    print """
    usage:
    python summarize_protein_matches.py <nonredundant_pep_file> <output_file>
    
    
    """
    sys.exit(-1)

if len(args) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()
track_dict = defaultdict(int)
    
with open(sys.argv[1], "r") as f, open(sys.argv[2], "w", 1) as out:
    for title, seq in fastaIO.FastaGeneralIterator(f):
        hit_class = ''
        if "plus_" in title:
            hit_class = title.rsplit("plus_", 1)[1]
        elif "minus_" in title:
            hit_class = title.rsplit("minus_", 1)[1]
        if hit_class == "?":
            hit_class = "Undetermined"
        track_dict[hit_class] += 1
        
    for key in track_dict:
        print>>out, key + "\t" + str(track_dict[key])
        
        
