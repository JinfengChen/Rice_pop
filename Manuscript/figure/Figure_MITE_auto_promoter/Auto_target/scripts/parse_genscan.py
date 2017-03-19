#!/usr/bin/env python

import sys
import os
import os.path

args = sys.argv[1:]

def usage():
    print """
    usage:
    
    python parse_genscan.py <genscan_output_file> <protein_seq_output>
    
    This script will parse the output from the genscan ab initio gene prediction program.
    
    """
    sys.exit(-1)

if len(args) != 1 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()

out_path = os.path.splitext(sys.argv[1])[0] + "_protein.fa"
with open(sys.argv[1], "r") as f, open(out_path, "w", 1) as out:
    seq_len = 0
    matrix = ''
    name = ''
    prot_num = 0
    protein = ''
    want = 0
    hit_end = 0
    next_seq = 0
    out_name = ''
    
    for line in f:
        line = line.strip()
        
        if "GENSCAN 1.0" in line:
            want = 0
            seq_len = 0
            matrix = ''
            name = ''
            prot_num = 0
            protein = ''
            next_seq = 0
            out_name = ''
            hit_end = 0
        
        if "Sequence" in line:
            line = line.split(" : ")
            name = line[0].split("Sequence ")[1]
            seq_len = int(line[1].split(" bp")[0])
            hit_end = seq_len - 10000
            
        elif "matrix" in line:
            matrix = line.split("matrix: ")[1].split(".smat")[0]
            
        elif " + " in line and line.startswith(tuple('0123456789')):
            line = line.replace("     ", " ")
            line = line.replace("    ", " ")
            line = line.replace("   ", " ")
            line = line.replace("  ", " ")
            info = line.split("+ ")[1].split(" ")
            #print "info[0]:", info[0]
            start = int(info[0].strip())
            end = info[1].strip()
            end = end.split(" ")[0]
            #print "end =", end
            end = int(end)
            
            if 10000 <= start <= hit_end or 10000 <= end <= hit_end:
                want = 1
                protein_name = line.split(".")[0]
        elif line[:1] == ">" and want == 1:
            if next_seq == 1:
                next_seq = 0
            pred_name = line.split("peptide_")[1].split("|")[0]
            if pred_name == protein_name:
                next_seq = 1
                out_name = line.split("|")[0] + "_genscan" + pred_name + "-" + matrix
                start_seq = 1
                
        elif next_seq == 1 and line != "":
            if start_seq == 1:
                if line[0] == "M":
                    print>>out, out_name + "\n" + line
                    start_seq = 0
                    continue
                else:
                    start_seq = 0
                    next_seq = 0
                
            else:
                print>>out, line
                
        
            
            
            
            
        
            
        
