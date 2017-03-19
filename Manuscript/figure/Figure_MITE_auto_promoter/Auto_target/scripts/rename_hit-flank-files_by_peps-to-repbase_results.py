#!/usr/bin/env python

import sys
import os
import os.path
import fastaIO
import fnmatch
from collections import OrderedDict

args = sys.argv[1:]
arg_len = len(args)

print "Argument length:", arg_len

def usage():
    print """
    usage:
    python rename_hit-flank-files_by_peps-to-repbase_results.py <DNA_TPase_match_file> <retro_match_file> <heli-mav_match_file> <no_match_file> <hit_seq_file> <flank_seq_file> <cluster_output_path1> <cluster_output_path2> <strand_in_match_titles?>
    
    The two cluster paths are optional. The hit and flank file processing can be skipped by using 'na' without quotes as the path. If the sequences to have protein hit info added contain strand information and the match files do not, it must be split off for the script to work. Putting any value with trigger this option.
    
    """
    sys.exit(-1)

if (len(args) != 6 and len(args) != 7 and len(args) != 8 and len(args) != 9) or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()

wanted_dict = {}

#import DNA match file
dna_in = open(sys.argv[1], "r")
info = dna_in.readlines()
c = 0
for line in info:
    line = line.strip()
    line = line.split("\t")
    if "_protein" in line[0]:
        name = line[0].split("_protein")[0]
    elif "_genscan" in line[0]:
        name = line[0].split("_genscan")[0]
    if line[3] == "?":
        if "SPM" in line[2] or "OSHOOTER" in line[2] or "PSL" in line[2] or "SmTRC1" in line[2]:
            line[3] = "CMC"
        elif "HARB" in line[2]:
            line[3] = "PIF_harbinger"
        else:
            line[2] = line[2].split(":")
            line[3] = "Uncertain:" + line[2][0]
    if "/" in line[3]:
        line[3] = line[3].replace("/", "_")
    new_name = "_" + line[3]
    if c < 4:
        print ' '.join(["DNA match:", name, new_name])
    if name not in wanted_dict:
        wanted_dict[name] = new_name
    c += 1
dna_in.close()
print "\n"

retro_in = open(sys.argv[2], "r")
info = retro_in.readlines()
c = 0
for line in info:
    line = line.strip()
    line = line.split("\t")
    if "_protein" in line[0]:
        name = line[0].split("_protein")[0]
    elif "_genscan" in line[0]:
        name = line[0].split("_genscan")[0]
    new_name = "_retro"
    if c < 4:
        print ' '.join(["Retro:", name, new_name])
    if name not in wanted_dict:
        wanted_dict[name] = new_name
    c += 1
retro_in.close()
print "\n"

heli_in = open(sys.argv[3], "r")
info = heli_in.readlines()
c = 0
for line in info:
    line = line.strip()
    line = line.split("\t")
    if "_protein" in line[0]:
        name = line[0].split("_protein")[0]
    elif "_genscan" in line[0]:
        name = line[0].split("_genscan")[0]
    ele = line[1].rsplit(":", 1)[1]
    new_name = "_" + ele
    if c < 4:
        print ' '.join(["Helitron:", name, new_name])
    if name not in wanted_dict:
        wanted_dict[name] = new_name
    c += 1
heli_in.close()
print "\n"
    
no_match_in = open(sys.argv[4], "r")
info = no_match_in.readlines()
c = 0
for line in info:
    line = line.strip()
    if "_protein" in line:
        name = line.split("_protein")[0]
    elif "_genscan" in line:
        name = line.split("_genscan")[0]
    new_name = "_Unknown"
    if c < 4:
        print ' '.join(["Unknown:", name, new_name])
    if name not in wanted_dict:
        wanted_dict[name] = new_name
    c += 1
no_match_in.close()
print "\n" 
#for key in wanted_dict:
#    print key, "  ", wanted_dict[key]

if sys.argv[5] != "na":
    c = 0
    #import hit sequence file
    hit_in = open(sys.argv[5], "r")
    hit_track = OrderedDict()
    for title, seq in fastaIO.FastaGeneralIterator(hit_in):
        if arg_len == 9:
            if "plus_" in title:
                title = title.rsplit("_plus", 1)[0]
            elif "minus_" in title:
                title = title.rsplit("_minus", 1)[0]
            
        else:
            if "plus_" in title:
                title = title.rsplit("plus_", 1)[0] + "plus"
            elif "minus_" in title:
                title = title.rsplit("minus_", 1)[0] + "minus"
            
        if c < 4:
            print "hit title:", title
        if title in wanted_dict:
            title = title + wanted_dict[title]
            hit_track[title] = seq
        else:
            #print "1, Title:", title
            title = title + "_unpredicted"
            hit_track[title] = seq
            
        c += 1
    hit_in.close()
    parts = os.path.splitext(sys.argv[5])
    hit_out = open(parts[0] + "_match-info" + parts[1], "w", 1)
    for keys in hit_track:
        print>>hit_out, ">" + keys + "\n" + hit_track[keys]
    hit_out.close()
    print "\n"

if sys.argv[6] != "na":
    #import flank sequence file
    flank_in = open(sys.argv[6], "r")
    flank_track = OrderedDict()
    c = 0
    for title, seq in fastaIO.FastaGeneralIterator(flank_in):
        if arg_len == 9:
            if "plus_" in title:
                title = title.rsplit("_plus", 1)[0]
            elif "minus_" in title:
                title = title.rsplit("_minus", 1)[0]
            
        else:
            if "plus_" in title:
                title = title.rsplit("plus_", 1)[0] + "plus"
            elif "minus_" in title:
                title = title.rsplit("minus_", 1)[0] + "minus"
        if c < 4:
            print "flank title:", title
        if title in wanted_dict:
            title = title + wanted_dict[title]
            flank_track[title] = seq
        else:
            title = title + "_unpredicted"
            flank_track[title] = seq
            
        c += 1
    flank_in.close()
    parts = os.path.splitext(sys.argv[6])
    flank_out = open(parts[0] + "_match-info" + parts[1], "w", 1)
    for keys in flank_track:
        print>>flank_out, ">" + keys + "\n" + flank_track[keys]
    flank_out.close()

if arg_len >= 7:
    print "Loop 7 yes!"
    d = 0
    base_file_list = os.listdir(sys.argv[7])
    base_dict = {}
    for item in base_file_list:
        base_dict[item] = 1
    for root, dirs, files in os.walk(sys.argv[7]):
        for filename in files:
            if fnmatch.fnmatch(filename, '*.msa') or fnmatch.fnmatch(filename, '*.group*split') or fnmatch.fnmatch(filename, '*.fa') or fnmatch.fnmatch(filename, '*.final'):
                fpath = os.path.join(root, filename)
                in_handle = open(fpath, "r")
                track_dict = OrderedDict()
                c = 0
                for title, seq in fastaIO.FastaGeneralIterator(in_handle):
                    if arg_len == 9:
                        if "_plus" in title:
                            title = title.rsplit("_plus", 1)[0]
                        elif "_minus" in title:
                            title = title.rsplit("_minus", 1)[0]
                        
                    else:
                        if "_plus" in title:
                            title = title.rsplit("_plus", 1)[0] + "_plus"
                        elif "_minus" in title:
                            title = title.rsplit("_minus", 1)[0] + "_minus"
                        
                    if c < 4 and d < 2:
                        print "Seven loop title:", title
                    
                    if title in wanted_dict:
                        title = title + wanted_dict[title]
                        track_dict[title] = seq
                    else:
                        title = title + "_unpredicted"
                        track_dict[title] = seq
                    c += 1
                in_handle.close()
                out_handle = open(fpath, "w", 1)
                for keys in track_dict:
                    print>>out_handle, ">" + keys + "\n" + track_dict[keys]
                out_handle.close()
            d += 1
            
if arg_len >= 8:
    print "Loop 8 yes!"
    d = 0
    for root, dirs, files in os.walk(sys.argv[8]):
        for filename in files:
            if fnmatch.fnmatch(filename, '*.fa') or fnmatch.fnmatch(filename, '*.msa') or fnmatch.fnmatch(filename, '*.group*split') or fnmatch.fnmatch(filename, '*.final'):
                fpath = os.path.join(root, filename)
                in_handle = open(fpath, "r")
                track_dict = OrderedDict()
                c = 0
                for title, seq in fastaIO.FastaGeneralIterator(in_handle):
                    if arg_len == 9:
                        if "_plus" in title:
                            title = title.rsplit("_plus", 1)[0]
                        elif "_minus" in title:
                            title = title.rsplit("_minus", 1)[0]
                        
                    else:
                        if "_plus" in title:
                            title = title.rsplit("_plus", 1)[0] + "_plus"
                        elif "_minus" in title:
                            title = title.rsplit("_minus", 1)[0] + "_minus"
                    if c < 4 and d < 2:
                        print "Eight loop title:", title
                        
                    if title in wanted_dict:
                        title = title + wanted_dict[title]
                        track_dict[title] = seq
                    else:
                        title = title + "_unpredicted"
                        track_dict[title] = seq
                        
                    c += 1
                in_handle.close()
                out_handle = open(fpath, "w", 1)
                for keys in track_dict:
                    print>>out_handle, ">" + keys + "\n" + track_dict[keys]
                out_handle.close()
            d += 1
            

