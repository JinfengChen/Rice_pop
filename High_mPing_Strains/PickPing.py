#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
from Bio import SeqIO
import glob

def usage():
    test="name"
    message='''
python PickPing.py --input Japonica_fastq_RelocaTEi_Pong/ERS470370_RelocaTEi


    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#repeat  Chr1:480846..480848     Junction_reads  ERR624499.2788059:start:5,ERR624507.3823168:start:5,ERR624505.1031664:end:5
#repeat  Chr1:480846..480848     Left_supporting_reads   
#repeat  Chr1:480846..480848     Right_supporting_reads  
def parse_support_reads(infile, support_inf):
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if len(unit) == 4:
                    reads = re.split(r',', unit[3])
                    support_inf[unit[1]][unit[2]] = reads
                else:
                    reads = []
                    support_inf[unit[1]][unit[2]] = reads

#Japonica_fastq_RelocaTEi_Pong/ERS470370_RelocaTEi/repeat/results/ALL.all_nonref_insert.gff
#Chr1    not.give        RelocaTE_i      480846  480848  .       -       .       ID=repeat_Chr1_480846_480848;TSD=TTA;Note=Non-reference, not found in reference;
#Right_junction_reads:2;Left_junction_reads:1;Right_support_reads:0;Left_support_reads:0;
def gff_parse(infile, flank_inf, support_inf):
    data = defaultdict(lambda : list())
    r = re.compile(r'\=')
    with open (infile, 'r') as filehd:
        for line in filehd: 
            line = line.rstrip()
            if len(line) > 2 and not line.startswith('#'): 
                unit  = re.split(r'\t',line)
                start = int(unit[3]) 
                end   = int(unit[4])
                chro  = unit[0]
                strand= unit[6]
                temp  = defaultdict(str)
                attrs = re.split(r';', unit[8])
                for attr in attrs:
                    #print attr
                    if not attr == '':
                        #print 'yes'
                        if r.search(attr):
                            idx, value = re.split(r'\=', attr)
                            temp[idx] = value
                        else:
                            idx, value = re.split(r'\:', attr)
                            temp[idx] = value
                Rjun    = temp['Right_junction_reads']
                Rsup    = temp['Right_support_reads']
                Ljun    = temp['Left_junction_reads']
                Lsup    = temp['Left_support_reads']
                #print '%s\t%s\t%s\t%s\t%s\t%s' %(repid, chro, start, end, repname, repfam)
                #print '%s\t%s\t%s' %(chro, start, end)
                repid   = '%s:%s..%s' %(chro, start, end)
                left_supporting_picks  = check_supporting_reads(support_inf[repid]['Left_supporting_reads'], repid, flank_inf)
                right_supporting_picks = check_supporting_reads(support_inf[repid]['Right_supporting_reads'], repid, flank_inf)
                if len(left_supporting_picks[repid]) > 0 and len(right_supporting_picks[repid]) > 0:
                    print 'Find Pong: %s' %(line)
                elif len(left_supporting_picks[repid]) > 0 or len(right_supporting_picks[repid]) > 0:
                    print 'Candidate Pong: %s' %(line) 
                else:
                    pass
    return data


def check_supporting_reads(reads_list, repid, flank_inf):
    data = defaultdict(lambda : list())
    #cover_int_ping = 0
    #start_int      = 23    #253 for Ping
    #end_int        = 5300  #5164 for Ping
    #start_snp      = 17    #16 for Ping
    start_int      = 253
    end_int        = 5164
    start_snp      = 16
    if len(reads_list) > 0:
        for read in reads_list:
            for i in [1, 2]:
                if not flank_inf[read][str(i)]['pos'] == '':
                    if flank_inf[read][str(i)]['pos'] == 'middle':
                        if repid == 'Chr1:480846..480848':
                            print '%s\t%s\t%s\t%s' %(repid, read, flank_inf[read][str(i)]['start'], flank_inf[read][str(i)]['end'])
                        if int(flank_inf[read][str(i)]['start']) >= start_int+10 and int(flank_inf[read][str(i)]['start']) <= end_int-10:
                            data[repid].append(read)
                        elif int(flank_inf[read][str(i)]['end']) >= start_int+10 and int(flank_inf[read][str(i)]['end']) <= end_int-10:
                            data[repid].append(read)
                    #elif flank_inf[read][str(i)]['pos'] == 'start' or flank_inf[read][str(i)]['pos'] == 'end':
                    #    if int(flank_inf[read][str(i)]['end']) == 5: #read mapped to 5primer of TE
                    #        if int(flank_inf[read][str(i)]['start']) < start_snp or int(flank_inf[read][str(i)]['start']) > start_snp and int(flank_inf[read][str(i)]['mismatch']) == 0:
                    #            data[repid].append(read)
        return data
    else:
        return data

#parse blatout file, if the reads were found in flankingreads we store match information also for further check
#Japonica_fastq_RelocaTEi_Pong/ERS470370_RelocaTEi/repeat/blat_output/ERR624495_1.te_repeat.blatout
def parse_blatout(blat_file, flank_inf):
    r        = re.compile(r'.*\/(\w+)\_(\d+)\.te\_repeat\.blatout')
    lib_n, lib_t = ['NA','0']
    if r.search(blat_file):
        lib_n = r.search(blat_file).groups(0)[0]
        lib_t = r.search(blat_file).groups(0)[1]
    #print 'blatout', lib_n, lib_t
    ##align_file
    with open (blat_file, 'r') as filehd:
        for i in range(5):
            next(filehd)
        for line in filehd:
            line = line.rstrip()
            unit = re.split(r'\t',line)
            match    = int(unit[0])
            mismatch = int(unit[1])
            strand   = unit[8]
            qName    = unit[9]
            qLen     = int(unit[10])
            qStart   = int(unit[11])
            qEnd     = int(unit[12]) - 1
            tName    = unit[13]
            tLen     = int(unit[14])
            tStart   = int(unit[15])
            #get all values into 1st base = 0 postion notation
            tEnd     = int(unit[16]) - 1
            if int(unit[17]) > 1:
                tStart = 0
                tEnd   = 0 
            boundary = 1 if int(qStart) == 0 or int(qEnd) + 1 == int(qLen) else 0
            #if qName == 'ERR624495.1563':
            #    print qName, lib_t, flank_inf[qName][str(lib_t)]['pos']
            if not flank_inf[qName][str(lib_t)]['pos'] == '':
                flank_inf[qName][str(lib_t)]['start'] = str(tStart)
                flank_inf[qName][str(lib_t)]['end']   = str(tEnd)
                flank_inf[qName][str(lib_t)]['mismatch'] = str(mismatch)
                #print qName, lib_t, tStart, tEnd, mismatch

#parse flankingReads.fq file to store these reads that matched to repeat confidently
#Japonica_fastq_RelocaTEi_Pong/ERS470370_RelocaTEi/repeat/flanking_seq/ERR624495_1.te_repeat.flankingReads.fq
#@ERR624495.2984685:middle
#@ERR624495.147060:start:5
def parse_flanking_fastq(fastq_file, flank_inf):
    r_middle = re.compile(r'(.*)\:middle')
    r_end    = re.compile(r'(.*)\:(start|end)\:(\d+)')
    r        = re.compile(r'.*\/(\w+)\_(\d+)\.te\_repeat\.flankingReads\.fq')
    lib_n, lib_t = ['NA','0']
    if r.search(fastq_file):
        lib_n = r.search(fastq_file).groups(0)[0]
        lib_t = r.search(fastq_file).groups(0)[1]
    count    = 3
    #print lib_n, lib_t
    with open (fastq_file, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            count += 1
            if count%4 == 0:
                read_name = str(line[1:])
                #print read_name
                if r_middle.search(read_name):
                    read_id = r_middle.search(read_name).groups(0)[0]
                    pos     = 'middle'
                    flank_inf[read_id][str(lib_t)]['pos'] = pos
                    #print read_id, lib_t, pos
                elif r_end.search(read_name):
                    read_id = r_end.search(read_name).groups(0)[0]
                    pos     = r_end.search(read_name).groups(0)[1]
                    end     = r_end.search(read_name).groups(0)[2]
                    flank_inf[read_id][str(lib_t)]['pos'] = pos
                    flank_inf[read_id][str(lib_t)]['end'] = end
                    #print read_id, lib_t, pos
                else:
                    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)
    
    flank_inf = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : str())))

    #parse flankingReads.fq
    #Japonica_fastq_RelocaTEi_Pong/ERS470370_RelocaTEi/repeat/flanking_seq/ERR624495_1.te_repeat.flankingReads.fq
    flankingreads = glob.glob('%s/repeat/flanking_seq/*.te_repeat.flankingReads.fq' %(args.input))
    for fread in flankingreads:
        #print fread
        parse_flanking_fastq(fread, flank_inf)
 
    #print 'CK, ERR624495.1563, %s' %(flank_inf['ERR624495.1563'][str(1)]['pos'])   
    #for read in sorted(flank_inf.keys()):
    #    for lib in sorted(flank_inf[read].keys()):
    #        print '%s\t%s\t%s' %(read, lib, flank_inf[read][lib]['pos'])
 
    #parse blatout
    #Japonica_fastq_RelocaTEi_Pong/ERS470370_RelocaTEi/repeat/blat_output/ERR624495_1.te_repeat.blatout
    blatouts =glob.glob('%s/repeat/blat_output/*.te_repeat.blatout' %(args.input)) 
    for bout in blatouts:
        parse_blatout(bout, flank_inf)   

    #for read in sorted(flank_inf.keys()):
    #    for lib in sorted(flank_inf[read].keys()):
    #        print '%s\t%s\t%s' %(read, lib, flank_inf[read][lib]['pos'])

    #parse supporting_reads for each insertion
    support_inf = defaultdict(lambda : defaultdict(lambda : list()))
    #Japonica_fastq_RelocaTEi_Pong/ERS470370_RelocaTEi/repeat/results/Chr1.repeat.reads.list
    support_reads = glob.glob('%s/repeat/results/Chr*.repeat.reads.list' %(args.input)) 
    for sread in support_reads:
        parse_support_reads(sread, support_inf)
 
    #parse gff file and check junction reads and supporting reads if they cover mPing/Ping/Pong difference area
    all_gff='%s/repeat/results/ALL.all_nonref_insert.gff' %(args.input)
    gff_parse(all_gff, flank_inf, support_inf)

if __name__ == '__main__':
    main()

