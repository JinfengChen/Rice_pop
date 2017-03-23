#!/usr/bin/env python

import os
import os.path
import sys
import datetime
import glob
import subprocess as subp
import argparse
import re
import fastaIO
import fnmatch
from collections import defaultdict

args = sys.argv[1:]

def usage():
    print """
    Usage: list_aTE_good_bad_mixed.py <parent_aTE_results_folder> <output_folder> <run_name>

    This script will parse all activeTE results in folders contained in the specified parent_aTE_results_folder, creating lists of elements for good, bad, conserved flanks, mixed, and unfinished results. These lists are created in the indicated output folder with run name as the files' prefix.
    """
    sys.exit(-1)

if len(args) != 3 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()



track_dict = {}
flank_dict = {}
group_dict = defaultdict(lambda: 'start')
unfinished = []

for root, dirs, Files in os.walk(sys.argv[1]):
    for i in dirs:
        if '.combined' in i:
            continue
        if '.group' not in i:
            dir_path = os.path.join(root, i)
            dir_contents = os.listdir(dir_path)
            base = ''
            bad = 0
            good = 0
            no_tsd = 0
            flank = 0
            left = 0
            right = 0
            both = 0
            for files in dir_contents:
                if "ggsearch" in files or ".txt" in files or ".blast.out" in files or ".trim" in files or ".intermediate" in files:
                    continue
                if not base:
                    base = os.path.split(files.split('.msa')[0])[1]
                if '.abort' in files:
                    bad = 1
                elif '.element_info' in files:
                    good = 1
                elif '.no_tsd' in files:
                    no_tsd = 1
                elif '.conserved_left_flank' in files:
                    flank = 1
                    left = 1
                elif '.conserved_right_flank' in files:
                    flank = 1
                    right = 1
                elif '.conserved_flanks' in files:
                    flank = 1
                    both = 1
                else:
                    continue
                    
            if bad == 1:
                if good == 1 or no_tsd == 1 or flank == 1:
                    track_dict[base] = 'mixed'
                else:
                    track_dict[base] = 'bad'
            elif good == 1:
                if no_tsd == 1 or flank ==1:
                    track_dict[base] = 'mixed'
                else:
                    track_dict[base] = 'good'
            elif no_tsd == 1:
                if flank == 1:
                    track_dict[base] = 'mixed'
                else:
                    track_dict[base] = 'no_tsd'
            elif flank == 1:
                if left == 1:
                    track_dict[base] = 'flank'
                    flank_dict[base] = 'left'
                if right == 1:
                    track_dict[base] = 'flank'
                    flank_dict[base] = 'right'
                if both == 1:
                    track_dict[base] = 'flank'
                    flank_dict[base] = 'both'
            elif bad == 0 and good == 0 and no_tsd == 0 and flank == 0:
                unfinished.append(dir_path)
        else:
            dir_path = os.path.join(root, i)
            dir_contents = os.listdir(dir_path)
            base = ''
            bad = 0
            good = 0
            no_tsd = 0
            flank = 0
            left = 0
            right = 0
            both = 0
            temp = []
            for files in dir_contents:
                if "ggsearch" in files or ".txt" in files or ".blast.out" in files or ".trim" in files or ".intermediate" in files:
                    continue
                if not base:
                    base = os.path.split(files.split('.msa')[0])[1]
                if '.abort' in files:
                    bad = 1
                elif '.element_info' in files:
                    good = 1
                elif '.no_tsd' in files:
                    no_tsd = 1
                elif '.conserved_left_flank' in files:
                    flank = 1
                    left = 1
                elif '.conserved_right_flank' in files:
                    flank = 1
                    right = 1
                elif '.conserved_flanks' in files:
                    flank = 1
                    both = 1
                else:
                    continue
                    
                if bad == 1:
                    if group_dict[base] == 'start': 
                        track_dict[base] = 'bad'
                        group_dict[base] = 'bad'
                        temp = [os.path.splitext(files)[0], "abort"]
                    
                    elif group_dict[base] == 'good' or group_dict[base] == 'no_tsd' or group_dict[base] == 'flank':
                        track_dict[base] = 'mixed'
                        group_dict[base] = 'mixed'
                        break

                        
                if good == 1:
                    if group_dict[base] == 'start':
                        track_dict[base] = 'good'
                        group_dict[base] = 'good'
                    
                    elif group_dict[base] == 'bad' or group_dict[base] == 'no_tsd' or group_dict[base] == 'flank':
                        track_dict[base] = 'mixed'
                        group_dict[base] = 'mixed'
                        break
            
                if no_tsd == 1:
                    if group_dict[base] == 'start':
                        track_dict[base] = 'no_tsd'
                        group_dict[base] = 'no_tsd'
                
                    elif group_dict[base] == 'good' or group_dict[base] == 'bad' or group_dict[base] == 'flank':
                        track_dict[base] = 'mixed'
                        group_dict[base] = 'mixed'
                        break
                
                if flank == 1:
                    if group_dict[base] == 'start':
                        if left == 1:
                            track_dict[base] = 'flank'
                            group_dict[base] = 'flank'
                            flank_dict[base] = 'left'
                        if right == 1:
                            track_dict[base] = 'flank'
                            group_dict[base] = 'flank'
                            flank_dict[base] = 'right'
                        if both == 1:
                            track_dict[base] = 'flank'
                            group_dict[base] = 'flank'
                            flank_dict[base] = 'both'
                
                    elif group_dict[base] == 'good' or group_dict[base] == 'bad' or group_dict[base] == 'no_tsd':
                        track_dict[base] = 'mixed'
                        group_dict[base] = 'mixed'
                        break
                        
            if bad == 0 and good == 0 and no_tsd == 0 and flank == 0:
                unfinished.append(dir_path)

            

gpath = sys.argv[2] + sys.argv[3] + ".good"
bpath = sys.argv[2] + sys.argv[3] + ".bad"
mixpath = sys.argv[2] + sys.argv[3] + ".mixed"
no_tsdpath = sys.argv[2] + sys.argv[3] + ".no_tsd"
flankpath = sys.argv[2] + sys.argv[3] + ".conserved_flanks"
unfinished_path = sys.argv[2] + sys.argv[3] + ".unfinished"

good_out = open(gpath, "w")
bad_out = open(bpath, "w")
mixed_out = open(mixpath, "w")
flank_out = open(flankpath, "w")
no_tsd_out = open(no_tsdpath, "w")

for keys in track_dict:
    if track_dict[keys] == 'good':
        print>>good_out, keys
    elif track_dict[keys] == 'bad':
        print>>bad_out, keys
    elif track_dict[keys] == 'flank':
        print>>flank_out, keys + "\t" + flank_dict[keys]
    elif track_dict[keys] == 'mixed':
        print>>mixed_out, keys
    elif track_dict[keys] == 'no_tsd':
        print>>no_tsd_out, keys

good_out.close()
bad_out.close()
flank_out.close()
mixed_out.close()
no_tsd_out.close()

unfinished_out = open(unfinished_path, "w")

for item in unfinished:
    print>>unfinished_out, item

unfinished_out.close()
