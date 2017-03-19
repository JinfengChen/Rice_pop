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
    print """Usage: recombine_aTE-out3.py <good_element_list> <parent_aTE_results_folder> <output_folder> <run_name>

This script will parse all activeTE results in folders contained in the specified parent_aTE_results_folder, creating lists of elements for good, bad, conserved flanks, mixed, and unfinished results. These lists are created in the indicated output folder with run name as the files' prefix."""
    sys.exit(-1)

if len(args) != 4 or sys.argv[1] == '-h' or sys.argv[1] == '-help' or sys.argv[1] == '-H' or sys.argv[1] == '-Help' or sys.argv[1] == '--h' or sys.argv[1] == '--help':
    usage()


if not os.path.exists(sys.argv[3]):
    os.mkdir(sys.argv[3])

#import good element list and store in dictionary
good_in = open(sys.argv[1], "r")
info = good_in.readlines()
good_dict = {}
flank_check = 0
for line in info:
    line = line.strip()
    if ".flank" in line:
        line = line.split(".flank")[0]
        flank_check = 1
    good_dict[line] = 1
good_in.close()

aborted_path = os.path.join(sys.argv[3], sys.argv[4] + "_recombine_aTE_aborted.txt")
aborted_out = open(aborted_path, "w", 1)

multiclass_path = os.path.join(sys.argv[3], sys.argv[4] + "_recombine_aTE_multiclass.txt")
multiclass_out = open(multiclass_path, "w", 1)

tsd_mis_path = os.path.join(sys.argv[3], sys.argv[4] + "_recombine_aTE_TSD-mismatches.txt")
tsd_mis_out = open(tsd_mis_path, "w", 1)

no_ele_info_path = os.path.join(sys.argv[3], sys.argv[4] + "_recombine_aTE_element_info_missing.txt")
no_ele_info_out = open(no_ele_info_path, "w", 1)

"""main_base = os.path.split(sys.argv[3])[0]
R_info_path = os.path.join(main_base, sys.argv[4] + "R_info.txt")
R_info_out = open(R_info_path, "w")"""

"""go through each good element, globbing all matching directories then
go through each of those directories to combine output from each group
store results in dictionary"""

for keys in good_dict:
    #to exclude initial msa files, add aTE to good element name for glob
    if flank_check == 1:
        search_query = os.path.join(sys.argv[2], "aTE_" + keys + ".flank" + "*")
    else:
        search_query = os.path.join(sys.argv[2], "aTE_" + keys + "*")
    dirs = glob.glob(search_query)
    group_len = len(dirs)
    
    print "\n" + keys + " group length = " + str(group_len) + "\nQuery:" + search_query
    insertion = defaultdict(list)
    removed = []
    left_tir = []
    right_tir = []
    element_info_dict = defaultdict(int)
    element_info_dict['tsd_consensus'] = ''
    element_info_dict['tsd_len'] = {}
    element_info_dict['classification'] = {}
    sanity_copy_count = 0
    sanity_tsd_count = defaultdict(int)
    tsd_issues_count = 0
    no_ele = 0
    no_ele_count = 0
    gff = []
    fasta = []
    tsd_issues = []
    tsd = defaultdict(list)
    override = 0
    tsd_skip = 0
    combine_out_folder = ''
    c = 0
    catch = 0
    for i in dirs:
        if os.path.isfile(i):
            continue
        if '.combined' in i:
            continue
        ibase = os.path.split(i)[1]
        print "i =", i, "\n"
        if '.group' in i:
            base = i.split(".group")[0]
            base2 = ibase.split(".group")[0]
        else:
            base = i
            base2 = ibase
        ele_info_path = ''    
        #make the combined out folder if it doesn't exist
        if combine_out_folder == '':
            combine_out_folder = os.path.join(sys.argv[3], base2 + ".combined")
            print "combined out folder:", combine_out_folder, "\n"
            
        if os.path.exists(combine_out_folder):
            if not os.path.isdir(combine_out_folder):
                os.mkdir(combine_out_folder)
        else:
            os.mkdir(combine_out_folder)
        
        skip = 0
        
        #make element info path, check for existance, and parse to store info if present
        out_contents = os.listdir(i)
        for files in out_contents:
            if fnmatch.fnmatch(files, '*.element_info'):
                ele_info_path = os.path.join(i, files) 
                print "Element info found:", ele_info_path, "\n"           
        copy_dict = {}
        if "cluster2633_" in ele_info_path:
            print "Yes, wanted cluster."
        if not ele_info_path or not os.path.exists(ele_info_path):
            print "Element info file not present in" + i + ", continuing to next part of group if split or next group if not."
            print>>no_ele_info_out, i
            no_ele = 1
            no_ele_count += 1
        
        else:
            no_ele = 0
            in_file = open(ele_info_path, "r")
            for line in in_file:
                line = line.strip()
                line = line.split("\t")
                
                #if first element info file, store all info. Otherwise, check new file's info against that already stored
                if c == 0:
                    print "First time through"
                    element_info_dict['name'] = keys
                    element_info_dict['copies'] += int(line[1])
                    element_info_dict['ele_id'] = float(line[2])
                    element_info_dict['ltir_con'] = line[3]
                    element_info_dict['ltir_id'] = float(line[4])
                    element_info_dict['rtir_con'] = line[5]
                    element_info_dict['rtir_id'] = float(line[6])
                    element_info_dict['tsd_len'] = defaultdict(dict)
                    if ", " in line[7]:
                        tsd_lens = line[7].split(", ")
                        tsd_cons = line[8].split(", ")
                        tsd_fracs = line[9].split(", ")
                        f = 0
                        for item in tsd_lens:
                            element_info_dict['tsd_len'][int(item)]['info'] = [tsd_cons[f], float(tsd_fracs[f])]
                            f += 1
                    else:
                        element_info_dict['tsd_len'][int(line[7])]['info'] = [line[8], float(line[9])]
                    
                    if ", " in line[10]:
                        class_split = line[10].split(", ")
                        for item2 in class_split:
                            #item_split = item2.split("_")[0]
                            element_info_dict['classification'][item2] = 1
                    else:
                        #item_split = line[10].split("_")[0]
                        element_info_dict['classification'][line[10]] = 1
                        print "First time initial classification:", line[10]
                    c += 1
                
                else:
                    print "Going through another in group"
                    if ", " in line[7]:
                        tsd_lens = line[7].split(", ")
                        tsd_cons = line[8].split(", ")
                        tsd_fracs = line[9].split(", ")
                        f = 0
                        for item in tsd_lens:
                            if int(item) in element_info_dict['tsd_len']:
                                print "TSD length in", ele_info_path, "matches that already stored in dictionary."
                                #element_info_dict['tsd_len'][int(item)][0] += (", " + tsd_cons[f])
                                element_info_dict['tsd_len'][int(item)]['info'][1] = (element_info_dict['tsd_len'][int(item)]['info'][1] + float(tsd_fracs[f]))/2
                                override = 1
                            elif int(item) not in element_info_dict['tsd_len']:
                                print "TSD length in", ele_info_path, "doesn't match that already stored in dictionary, aborting the processing of this group and continuing. Please investigate manually."
                                tsd_skip = 1
                            elif int(item) in element_info_dict['tsd_len'] and tsd_cons[f] != element_info_dict['tsd_len'][int(item)]['info'][0]:
                                print "TSD consensus in", ele_info_path, "doesn't match that already stored in dictionary. However, the TSD length matches so combining will continue. Please investigate manually though."
                                #element_info_dict['tsd_len'][int(item)][0] += (", " + tsd_cons[f])
                                element_info_dict['tsd_len'][int(item)]['info'][1] = (element_info_dict['tsd_len'][int(item)]['info'][1] + float(tsd_fracs[f]))/2
                                override = 1
                            f += 1
                    else:
                        if int(line[7]) in element_info_dict['tsd_len']:
                            element_info_dict['tsd_len'][int(line[7])]['info'][1] = (float(element_info_dict['tsd_len'][int(line[7])]['info'][1]) + float(line[9]))/2
                            override = 1
                        elif int(line[7]) not in element_info_dict['tsd_len']:
                            print "TSD length in", ele_info_path, "doesn't match that already stored in hash, aborting the processing of this group and continuing. Please investigate manually."
                            tsd_skip = 1
                        elif int(line[7]) in element_info_dict['tsd_len'] and element_info_dict['tsd_len'][int(line[7])]['info'][0] != line[8]:
                            print "TSD consensus in", ele_info_path, "doesn't match that already stored in hash. However, the TSD length matches so combining will continue. Please investigate manually though."
                            element_info_dict['tsd_len'][int(line[7])]['info'][1] = (float(element_info_dict['tsd_len'][int(line[7])]['info'][1]) + float(line[9]))/2
                            override = 1
                        
                            
                    if tsd_skip == 1 and override == 0:
                        print>>tsd_mis_out, "TSDs consensus and length not matching:", ele_info_path
                        break
                    element_info_dict['copies'] += int(line[1])
                    element_info_dict['ele_id'] = (element_info_dict['ele_id'] + float(line[2]))/2
                    element_info_dict['ltir_id'] = (element_info_dict['ltir_id'] + float(line[4]))/2
                    element_info_dict['rtir_id'] = (element_info_dict['rtir_id'] + float(line[6]))/2
                
                    
                    if ", " in line[10]:
                        class_split = line[10].split(", ")
                        for item2 in class_split:
                            #item_split = item2.split("_")[0]
                            if item2 not in element_info_dict['classification']:
                                print "Classification of", item2, "in", ele_info_path, "doesn't match that already stored in hash, appending new classification. Please investigate manually though."
                                element_info_dict['classification'][item2] = 1
                                catch = 1
                            
                    else:
                        #item_split = line[10].split("_")[0]
                        if  not line[10] in element_info_dict['classification']:
                            print "Classification of", line[10], "in", ele_info_path, "doesn't match that already stored in hash, a."
                            element_info_dict['classification'][line[10]] = 1
                            catch = 1
                    if catch == 1:
                        print>>multiclass_out, "Different classifications found between groups:", ele_info_path
                        
            
            if no_ele == 1:
                break
            
            out_contents = []
            #go through rest of the group output folder contents, seleting files to be combined
            out_contents = os.listdir(i)
            #print "out content length:", len(out_contents)
            for files in out_contents:
                
                if fnmatch.fnmatch(files, '*.fasta'):
                    fpath = os.path.join(i, files)
                    in_file = open(fpath, "r")
                    for line in in_file:
                        line = line.strip()
                        fasta.append(line)
                    in_file.close()
                    in_file = open(fpath, "r")
                    for title, seq in fastaIO.FastaGeneralIterator(in_file):
                        #print "copy title:", title
                        element_info_dict['total_len'] += len(seq)
                        sanity_copy_count += 1
                        copy_dict[title] = 1
                    print "copy count now:", sanity_copy_count
                    in_file.close()
                    break
            
            out_contents = []
            #go through rest of the group output folder contents, seleting files to be combined
            out_contents = os.listdir(i)
            for files in out_contents:
                for keys in element_info_dict['tsd_len']:
                    if fnmatch.fnmatch(files, '*.insertion-site' + str(keys) + '.fa'):
                        fpath = os.path.join(i, files)
                        in_file = open(fpath, "r")
                        for line in in_file:
                            line = line.strip()
                            insertion[keys].append(line)
                        in_file.close()
                        
                    if fnmatch.fnmatch(files, '*.tsd' + str(keys) + '.fa'):
                        fpath = os.path.join(i, files)
                        in_file = open(fpath, "r")
                        for line in in_file:
                            line = line.strip()
                            tsd[keys].append(line)
                        in_file.close()
                        in_file = open(fpath, "r")
                        for title, seq in fastaIO.FastaGeneralIterator(in_file):
                            #print "tsd title:", title
                            if title in copy_dict:
                                if copy_dict[title] == 1:
                                    sanity_tsd_count[keys] += 1
                                    copy_dict[title] = 0
                        in_file.close()
                
                if fnmatch.fnmatch(files, '*.gff'):
                    fpath = os.path.join(i, files)
                    in_file = open(fpath, "r")
                    for line in in_file:
                        line = line.strip()
                        gff.append(line)
                    in_file.close()
                
                if fnmatch.fnmatch(files, '*.left-tir.fa'):
                    fpath = os.path.join(i, files)
                    in_file = open(fpath, "r")
                    for line in in_file:
                        line = line.strip()
                        left_tir.append(line)
                    in_file.close()
                    
                if fnmatch.fnmatch(files, '*.right-tir.fa'):
                    fpath = os.path.join(i, files)
                    in_file = open(fpath, "r")
                    for line in in_file:
                        line = line.strip()
                        right_tir.append(line)
                    in_file.close()
                
                if fnmatch.fnmatch(files, '*.removed_sequences'):
                    fpath = os.path.join(i, files)
                    in_file = open(fpath, "r")
                    for line in in_file:
                        line = line.strip()
                        removed.append(line)
                    in_file.close()
            
                if fnmatch.fnmatch(files, '*.TSD_issues.info'):
                    fpath = os.path.join(i, files)
                    in_file = open(fpath, "r")
                    for line in in_file:
                        line = line.strip()
                        if line[0] == ">":
                            tsd_issues_count += 1
                        tsd_issues.append(line)
                    in_file.close()
            
            
    if group_len > 1:
        if no_ele_count == group_len:
            print "Either there are no element info files for the entire group or tsd length and consensus are off between all but one group. Investigate manually."
            print>>aborted_out, base
            continue
    
    """Do some sanity checks on counts and calculations. If all checks out,
    print combined files out to combined folder"""
    
    if element_info_dict['copies'] != sanity_copy_count:
        print "Copy count in dict,", element_info_dict['copies'], ", is not equal to sanity copy count," + str(sanity_copy_count) + "."
        #if element_info_dict['copies'] == sanity_copy_count + tsd_issues_count:
    for keys in element_info_dict['tsd_len']:        
        tsd_frac = sanity_tsd_count[keys]/float(sanity_copy_count)
        element_info_dict['tsd_len'][keys]['total_tsd_frac'] = tsd_frac
        if float(element_info_dict['tsd_len'][keys]['info'][1]) != float(tsd_frac):
            print "Manually calculated TSD fraction, " + str(tsd_frac) + ", is not equal to that from dictionary, " + str(element_info_dict['tsd_len'][keys]['info'][1]) + "."
    
    #setup output file paths    
    
    element_info_path = os.path.join(combine_out_folder, base2 + ".element_info_combine")
    Rinfo_path = os.path.join(combine_out_folder, base2 + "_Rinfo.tab")
    
    class_string = ''
    tsd_len_string = ''
    tsd_con_string = ''
    total_tsd_frac_string = ''
    class_count = 0
    for keys in element_info_dict['classification']:
        print "classification key:", keys
        class_string += keys + ", "
        class_count += 1
    class_string = class_string[:-2]
    #element_info_dict['classification'] = class_string
    combined_tsd_frac = 0
    for keys in element_info_dict['tsd_len']:
        tsd_len_string += str(keys) + ", "
        tsd_con_string += element_info_dict['tsd_len'][keys]['info'][0] + ", "
        total_tsd_frac_string += str(round(element_info_dict['tsd_len'][keys]['total_tsd_frac'], 3)) + ", "
        combined_tsd_frac += element_info_dict['tsd_len'][keys]['total_tsd_frac']
    tsd_len_string = tsd_len_string[:-2]
    tsd_con_string = tsd_con_string[:-2]
    total_tsd_frac_string = total_tsd_frac_string[:-2]
    combined_tsd_frac = round(combined_tsd_frac, 3)
        
    
    element_info_out = open(element_info_path, "w")
    print>>element_info_out, "\t".join([element_info_dict['name'], str(element_info_dict['copies']), str(round(element_info_dict['ele_id'], 3)), element_info_dict['ltir_con'], str(round(element_info_dict['ltir_id'], 3)), element_info_dict['rtir_con'], str(round(element_info_dict['rtir_id'], 3)), tsd_len_string, tsd_con_string, total_tsd_frac_string, class_string, str(element_info_dict['total_len'])])
    
    Rinfo_out = open(Rinfo_path, "w")
    header = "\t".join(["species", "superfamily", "family", "copies", "family_length", "family_id", "left_tir_id", "right_tir_id", "total_tsd_fraction", "median_ident_copies", "max_ident_copies", "min_ident_copies"])
    print>>Rinfo_out, header
    
    if class_count > 1 and catch > 0:
        superfamily = "Multiple"
    else:
        superfamily = class_string
            
    if element_info_dict['tsd_frac'] > 1:
        element_info_dict['tsd_frac'] = 1
        
    if element_info_dict['total_tsd_frac'] > 1:
        element_info_dict['total_tsd_frac'] = 1
                
    print>>Rinfo_out, "\t".join([sys.argv[4], superfamily, element_info_dict['name'], str(element_info_dict['copies']), str(element_info_dict['total_len']), str(round(element_info_dict['ele_id'], 3)), str(round(element_info_dict['ltir_id'], 3)), str(round(element_info_dict['rtir_id'], 3)), str(round(combined_tsd_frac, 3)), "NA", "NA", "NA"])
    
    
    for keys in element_info_dict['tsd_len']:
        tsd_path = os.path.join(combine_out_folder, base2 + "_tsd" + str(keys) + ".fa")
        tsd_out = open(tsd_path, "w")
        for line in tsd[keys]:
            print>>tsd_out, line
        tsd_out.close()
        
        insertion_path = os.path.join(combine_out_folder, base2 + ".insertion-site" + str(keys) + ".fa")
        insertion_out = open(insertion_path, "w")
        for line in insertion[keys]:
            print>>insertion_out, line
        insertion_out.close()
    
    tsd_issues_path = os.path.join(combine_out_folder, base2 + ".TSD_issuse.info")
    tsd_issues_out = open(tsd_issues_path, "w")
    for line in tsd_issues:
        print>>tsd_issues_out, line
    tsd_issues_out.close()
    
    left_tir_path = os.path.join(combine_out_folder, base2 + ".left-tir.fa")
    left_tir_out = open(left_tir_path, "w")
    for line in left_tir:
        print>>left_tir_out, line
    left_tir_out.close()
    
    right_tir_path = os.path.join(combine_out_folder, base2 + ".right-tir.fa")
    right_tir_out = open(right_tir_path, "w")
    for line in right_tir:
        print>>right_tir_out, line
    right_tir_out.close()
    
    gff_path = os.path.join(combine_out_folder, base2 + ".gff")
    gff_out = open(gff_path, "w")
    for line in gff:
        print>>gff_out, line
    gff_out.close()
    
    removed_seqs_path = os.path.join(combine_out_folder, base2 + ".removed_sequences")
    removed_seqs_out = open(removed_seqs_path, "w")
    for line in removed:
        print>>removed_seqs_out, line
    removed_seqs_out.close()
    
    fasta_path = os.path.join(combine_out_folder, base2 + ".fasta")
    fasta_out = open(fasta_path, "w")
    for line in fasta:
        print>>fasta_out, line
    fasta_out.close()

aborted_out.close()
tsd_mis_out.close()
multiclass_out.close()
no_ele_info_out.close()
Rinfo_out.close()
