#!/usr/bin/env python

import sys
import os
import re
import fnmatch
import os.path
import subprocess as subp
import fastaIO

args = sys.argv[1:]


def usage():
    print
"""
usage:

python separate_sequence_by-list.py <wanted_seq_list> <original_seq_file> <output_sequence_file>

"""

wanted_dict = {}

#import wanted list
in_handle = open(sys.argv[1], "r")
info = in_handle.readlines()

for line in info:
    line = line.strip()
    wanted_dict[line] = 1
in_handle.close()

#import original sequence file
in_handle2 = open(sys.argv[2], "r")
out_handle = open(sys.argv[3], "w")
for title, seq in fastaIO.FastaGeneralIterator(in_handle2):
    if title in wanted_dict:
        print>>out_handle, ">" + title + "\n" + seq
in_handle2.close()
out_handle.close()





