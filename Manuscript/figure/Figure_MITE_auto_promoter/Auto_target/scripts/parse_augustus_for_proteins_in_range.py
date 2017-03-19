#!/usr/bin/env python

import sys
import os
import os.path
import fastaIO

args = sys.argv[1:]

def usage():
    print """
Usage: parse_augustus_for_proteins_in_range.py <Augustus_output_gff>

This script will parse Augustus output for predictions in initial hit region (assumes 10kb flanks) and generates a fasta files of those predictions and a list of sequences without prediction in the region.
"""
    sys.exit(-1)

if len(args) != 1 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()

protein_list = []
protein_dict = {}
track_dict = {}
name = ''
prot_num = 0
protein = ''
next_seq = 0
cds_count = 0
want = 0
version = ''
seq_len = ''

with open(sys.argv[1], "r") as f:
    for line in f:
        line = line.strip()
        #print line
        
        if line[0] != "#":
            if "AUGUSTUS\tgene\t" in line:
                loc = line.split("gene\t")
                #print "\n"
                #print loc, "\n"
                #for i in loc:
                #    print i, "\n"
                loc = loc[1]
                loc = loc.split("\t")
                start = int(loc[0])
                end = int(loc[1])
                if (start <= 10000 and end >= (seq_len - 10000)) or ((10000 - start) <= 1500 and (start < (seq_len - 10500))):
                    want = 1
                    track_dict[name] = 1
                    #print "Found a wanted gene."
        
        if line[0] != "#":
            if "CDS" in line and want == 1:
                cds_count += 1
                #print "Found a CDS. Current CDS count is: " + str(cds_count)
        
        if " version. Using" in line:
            version = line.split(" version. Using")[0].split(" ")[1]
            
        if "prediction on sequence number" in line:
            #print line
            name = line.split("name = ")[1]
            #print name
            name = name.split(") ----")[0]
            track_dict[name] = 0
            prot_num = 0
            seq_len = int(line.split(",")[0].split("length = ")[1])
            #print "Seq len =", seq_len
            #print "Found prediction for " + name
            
        elif "start gene" in line:
            prot_num += 1
            #print "Found the start of a gene. Protein number is " + str(prot_num)
        
        if want == 1:    
            if "protein sequence = [" in line:
                #print "Found actual predicted sequnce."
                seq = line.split(" = [")[1]
                protein += seq
                next_seq = 1
                
            elif "end gene" in line:
                protein_list.append(">" + name + "_protein" + str(prot_num) + "_" + str(cds_count) + "-exons" + "_" + version + "\n" + protein[:-1])
                protein_dict[name] = 1
                num_prots = str(len(protein_list))
                #print "Reached the end of the prediction. Current number of proteins in list: " + num_prots
                protein = ''
                next_seq = 0
                cds_count = 0
                want = 0
                
            elif next_seq == 1:
                seq = line.strip("# ")
                protein += seq
                #print "Found more sequence."

out_pep_path = os.path.splitext(sys.argv[1])[0] + "_protein.fa"
out_no_path = os.path.splitext(sys.argv[1])[0] + "_no-protein.txt"
out_pep = open(out_pep_path, "w")
for item in protein_list:
    print>>out_pep, item
out_pep.close()

with open(out_no_path, "w", 1) as no_pep:
    for key in track_dict:
        if key not in protein_dict and track_dict[key] == 0:
            print>>no_pep, key

