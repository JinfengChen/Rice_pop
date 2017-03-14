#!/usr/bin/env python

import os
import os.path
import sys
import fnmatch
from collections import defaultdict


args = sys.argv[1:]

def usage():
    print """
    usage:
    
    python categorize_all_aTE_results_by_group.py <aTE_results_parent_folder> <output_folder> <run_name>
    
    example:
    python categorize_all_aTE_results_by_group.py /bigdata/bradc/aTE2/aedes/ /bigdata/bradc/aTE2/ aedes
    
    """
    sys.exit(-1)
    
if len(args) != 3 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()
    


unfinished = defaultdict(dict)
aTE_content = os.listdir(sys.argv[1])
redo_out = open(os.path.join(sys.argv[2], sys.argv[3] + "_aTE_redo.txt"), "w")

for i in aTE_content:
    ipath = os.path.join(sys.argv[1], i)
    if os.path.isdir(ipath):
        base = ipath.split("aTE_")[1]
        if ".group" in base:
            base = base.split(".group")[0]
        ele = 0
        tsd = 0
        abort = 0
        conserved = 0
        files = os.listdir(ipath)
        for item in files:
            if '.element_info' in item:
                ele = 1
            elif '.no_tsd' in item:
                tsd = 1
            elif '.abort' in item:
                abort = 1
            elif 'conserved' in item:
                conserved = 1
        
        if (ele == 0 and tsd == 0 and abort == 0 and conserved == 0) or len(files) < 3:
            unfinished[base]['empty'] = 1
            print "empty:", i
            print>>redo_out, ipath
        elif ele == 1 and tsd == 0 and abort == 0 and conserved == 0:
            unfinished[base]['class'] = 1
            print "class:", i
        elif ele == 0 and tsd == 1 and abort == 0 and conserved == 0:
            unfinished[base]['tsd'] = 1
            print "tsd:", i
        elif ele == 0 and tsd == 0 and abort == 1 and conserved == 0:
            unfinished[base]['abort'] = 1
            print "abort:", i
        elif ele == 0 and tsd == 0 and abort == 0 and conserved == 1:
            unfinished[base]['conserved'] = 1
            print "conserved:", i
        elif (ele == 1 and (tsd == 1 or abort == 1 or conserved == 1)) or (tsd == 1 and (ele == 1 or abort == 1 or conserved == 1)) or (abort == 1 and (tsd == 1 or ele == 1 or conserved == 1)) or (conserved == 1 and (tsd == 1 or ele == 1 or abort == 1)):
            unfinished[base]['multi'] = 1
            print "multi:", i

multi_out = open(os.path.join(sys.argv[2], sys.argv[3] + "_aTE_cat-multi.txt"), "w")
class_out = open(os.path.join(sys.argv[2], sys.argv[3] + "_aTE_cat-class.txt"), "w")
tsd_out = open(os.path.join(sys.argv[2], sys.argv[3] + "_aTE_cat-tsd.txt"), "w")
abort_out = open(os.path.join(sys.argv[2], sys.argv[3] + "_aTE_cat-abort.txt"), "w")
conserved_out = open(os.path.join(sys.argv[2], sys.argv[3] + "_aTE_cat-conserved.txt"), "w")
empty_out = open(os.path.join(sys.argv[2], sys.argv[3] + "_aTE_cat-empty.txt"), "w")

for base in unfinished:
    unfinished_len = len(unfinished[base])
    print base, "length:", unfinished_len
    if len(unfinished[base]) > 1:
        print>>multi_out, base
    else:
        for keys in unfinished[base]:
            if keys == 'empty':
                print>>empty_out, base
            elif keys == 'class':
                print>>class_out, base
            elif keys == 'tsd':
                print>>tsd_out, base
            elif keys == 'abort':
                print>>abort_out, base
            elif keys == 'conserved':
                print>>conserved_out, base
            elif keys == 'multi':
                print>>multi_out, base

multi_out.close()
class_out.close()
tsd_out.close()
abort_out.close()
conserved_out.close()
empty_out.close()
