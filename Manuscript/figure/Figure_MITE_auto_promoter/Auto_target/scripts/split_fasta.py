import sys
import os
import re
import fnmatch
import os.path
import subprocess as subp
import fastaIO

args = sys.argv[1:]

def usage():
    print """Usage: split_fasta.py <fasta_file> <output_folder>

This script will individually copy each sequence in the specified fasta file into new files in the indicated output folder."""
    sys.exit(-1)

if len(args) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()

in_handle = open(sys.argv[1], "r")

if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])

for title, seq in fastaIO.FastaGeneralIterator(in_handle):
    out_handle = open(os.path.join(sys.argv[2], title + ".fa"), 'w')
    seq = fastaIO.SplitLongString(seq, 60)
    print>>out_handle, ">" + title + "\n" + seq
    out_handle.close()
