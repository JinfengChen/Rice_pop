import sys
import os
import re
import fnmatch
import os.path
import fastaIO
import glob

args = sys.argv[1:]

def usage():
    print """Usage: python trim_flanks_directory.py <sequence_folder> <trim_length>

This script will remove the specified trim length from each end of every sequence in every file contained in the specified sequence folder."""
    sys.exit(-1)

if len(args) != 2 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()

files = os.listdir(sys.argv[1])

for i in files:
    if fnmatch.fnmatch(i, '*.fa') and "_trimmed" not in i:
        fpath = os.path.join(sys.argv[1], i)
        base = os.path.splitext(fpath)[0]
        out_path = base + "_trimmed-" + sys.argv[2] + ".fa"
        if os.path.exists(out_path) and os.path.isfile(out_path):
            continue
        glob_path = base + "_trimmed-" + sys.argv[2] + "_*" + ".fa"
        glob_list = glob.glob(glob_path)
        if len(glob_list) > 0:
            continue
        with open(fpath, "r") as f, open(out_path, "w", 1) as out_handle:
            for title, seq in fastaIO.FastaGeneralIterator(f):
                seq = seq[int(sys.argv[2]):-int(sys.argv[2])]
                seq = fastaIO.SplitLongString(seq, 60)
                print>>out_handle, ">" + title + "\n" + seq

