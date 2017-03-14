import sys
import os
import re
import fnmatch
import os.path
import subprocess as subp
import fastaIO

if not os.path.isfile(sys.argv[1]):
    print 'specify the input fasta file'
    exit(1)

in_name = sys.argv[1]
in_file = os.path.split(in_name)[1]
in_trim = os.path.splitext(in_file)[0]
out_dir = os.path.split(in_name)[0]
in_handle = open(in_name, "r")
c = 1
ofile = open('%s.split.list' %(os.path.splitext(in_name)[0]), 'w')
for title, seq in fastaIO.FastaTitleStandardization(in_handle):
    #out_handle = open(os.path.join(out_dir, in_trim + "_split" + str(c) + ".fa"), 'w')
    #print>>out_handle, ">" + title, "\n", seq
    print >> ofile, '%s_split%s\t%s' %(in_trim, str(c), title)
    c += 1
    #out_handle.close()
in_handle.close()
ofile.close()
