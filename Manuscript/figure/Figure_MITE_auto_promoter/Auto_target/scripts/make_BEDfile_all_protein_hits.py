#!/usr/bin/env python

import sys
import os
import fnmatch
import os.path
import subprocess as subp
import fastaIO
import re

args = sys.argv[1:]

def usage():
    print """
usage:
python make_BEDfile_all_protein_hits.py <TARGeT_protein_search_out_folder> <output_BEDfile> <genome_file> <output_flank_file> <output_hit_file>

example:

python make_BEDfile_all_protein_hits.py /shared/stajichlab/projects/mosquito/target/out/Aedes/protein/Last/ /shared/stajichlab/projects/mosquito/target/out/Aedes/protein/Last/all_pep-hits.bed /shared/stajichlab/projects/mosquito/target/genomes/Aedes.fa /shared/stajichlab/projects/mosquito/target/out/Aedes/protein/Last/nonredundant_pep_union-10kb.fa /shared/stajichlab/projects/mosquito/target/out/Aedes/protein/Last/nonredundant_pep_union-hits.fa
"""
    sys.exit(-1)

bed_list = []

pat = re.compile(r"Sbjct:(.+)[_| ]Length.+Location:\(([0-9]*)[_|\s]*-[_|\s]*([0-9]*)\).*Direction:(.+)")

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        if fnmatch.fnmatch(filename, '*.flank'):
            fpath = os.path.join(root, filename)
            in_handle = open(fpath, "r")
            for title, seq in fastaIO.FastaGeneralIterator(in_handle):
                m = pat.search(title)
                if m:
                    contig = m.group(1)
                    start = m.group(2)
                    if int(start) > 0:
                        start = str(int(start)-1)
                    end = m.group(3)
                    strand = m.group(4)
                    if strand == 'plus':
                        strand = "+"
                    elif strand == 'minus':
                        strand = "-"
                    
                    bed_list.append("\t".join([contig, start, end, title, "1", strand])) 
                else:
                    print "Couldn't find locus information in title:", title
                    exit(1)
                
            in_handle.close()
            
with open(sys.argv[2], "w", 1) as out:
    for i in bed_list:
        print>>out, i
sorted_out_path = os.path.splitext(sys.argv[2])[0] + "_sorted.bed"
sorted_out = open(sorted_out_path, "w", 1)
subp.call(["sort", "-V", "-k1,1", "-k2,2", sys.argv[2]], stdout=sorted_out)
sorted_out.close()

union_out_path = os.path.splitext(sys.argv[2])[0] + "_union.bed"
union_out = open(union_out_path, "w", 1)
subp.call(["bedtools", "merge", "-i", sorted_out_path, "-s", "-nms", "-scores", "median"], stdout=union_out)
union_out.close()

genome_dict = {}
with open(sys.argv[3], "r") as genome_in:
    for title, seq in fastaIO.FastaGeneralIterator(genome_in):
        title = title.split(" ")[0]
        genome_dict[title] = seq

bed_list = []
c = 1
union_final = os.path.splitext(union_out_path)[0] + "_renamed.bed"
with open(union_out_path, "r") as union_in, open(sys.argv[4], "w", 1) as flank_out, open(sys.argv[5], "w", 1) as hit_out, open(union_final, "w", 1) as final_out:
    for line in union_in:
        line = line.strip()
        line = line.split("\t")
        contig = line[0]
        start = line[1]
        start_adj = str(int(start)+1)
        end = line[2]
        strand = line[5]
        strand2 = ''
        if strand == "+":
            strand2 = "plus"
        else:
            strand2 = "minus"
        title = "pep-hit" + str(c) + "_" + contig + "_" + start_adj + "_" + end + "_" + strand2
        flank_seq = fastaIO.sequence_retriever(contig, int(start), int(end), 10000, genome_dict)
        seq = fastaIO.sequence_retriever(contig, int(start), int(end), 0, genome_dict)
        if strand == "-":
            seq = fastaIO.reverse_complement(seq)
            flank_seq = fastaIO.reverse_complement(flank_seq)
        print>>flank_out, ">" + title + "\n" + flank_seq
        print>>hit_out, ">" + title + "\n" + seq
        print>>final_out, "\t".join([contig, start, end, title, "1", strand])
        c += 1

union_final_sort_path = os.path.splitext(union_out_path)[0] + "_renamed_sorted.bed"
union_final_sort_out = open(union_final_sort_path, "w", 1)
subp.call(["sort", "-V", "-k1,1", "-k2,2", union_final], stdout=union_final_sort_out)
union_final_sort_out.close()
