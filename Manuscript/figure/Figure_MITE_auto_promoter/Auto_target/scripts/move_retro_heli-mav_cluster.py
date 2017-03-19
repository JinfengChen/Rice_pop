#!/usr/bin/env python

import sys
import os
import os.path
import fastaIO
import fnmatch
import shutil

args = sys.argv[1:]

def usage():
    print """
    usage:
    python move_retro-heli-mav_cluster.py <Top_folder_to_traverse> <Destination_folder> <run_name>
    
    """
    sys.exit(-1)

if len(args) != 3 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()
    
files = os.listdir(sys.argv[1])
remove_list = open(sys.argv[1] + "_" + sys.argv[3] +"_unwanted_cluster_seqs.txt", "w", 1)
for filename in files:
    if fnmatch.fnmatch(filename, '*.fa') or fnmatch.fnmatch(filename, '*.group*split') or fnmatch.fnmatch(filename, '*.msa'):
        fpath = os.path.join(sys.argv[1], filename)
        catch = 0
        uncatch = 0
        temp_list = []
        if os.path.isfile(fpath):
            in_handle = open(fpath, "r")
            for title, seq in fastaIO.FastaGeneralIterator(in_handle):
                temp_list.append(title)
                if "_retro" in title or "Helitron" in title or "Maverick" in title:
                    print "retro-heli-mav:", title
                    catch += 1
                else:
                    if "unpredicted" in title or "Unknown" in title:
                        print "unpred-unknown:", title
                        continue
                    else:
                        print "DNA:", title
                        uncatch += 1
            print "\n\ncatch:", catch, "uncatch:", uncatch, "   " + filename + "\n"
            if catch == 0 or uncatch > catch:
                catch = 0
                uncatch = 0
                continue
            elif catch >= 1 and catch > uncatch:
                try:
                    shutil.move(fpath, sys.argv[2])
                except:
                    os.remove(fpath)
                if '.msa' in filename:
                    aTE = os.path.join(sys.argv[1], "aTE_" + os.path.splitext(filename)[0])
                    if os.path.isdir(aTE):
                        try:
                            shutil.move(aTE, sys.argv[2])
                        except:
                            shutil.rmtree(aTE)
                    for line in temp_list:
                        print>>remove_list, line
                catch = 0
                uncatch = 0
                    
                
