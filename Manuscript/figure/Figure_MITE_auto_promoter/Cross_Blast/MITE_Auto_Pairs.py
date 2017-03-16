#!/opt/Python/2.7.3/bin/python
import sys
from collections import defaultdict
import numpy as np
import re
import os
import argparse
import glob
from Bio import SeqIO
sys.path.append('/rhome/cjinfeng/BigData/software/ProgramPython/lib')
from utility import gff_parser, createdir

def usage():
    test="name"
    message='''
python MITE_Auto_Pairs.py --input MITE2Auto.blast.table

Parse BLAST table of MITE search aganist Autonomous elements. Generate a list of MITE and autonamous pairs.
Input:
Query_id	Query_length	Query_start	Query_end	Subject_id	Subject_length	Subject_start	Subject_end	Identity	Positive	Gap	Align_length	Score	E_value	Query_annotation	Subject_annotation
rice_2_28804	342	78	341	pep-hit183_Chr6_22499070_22499586_plus	20518	3554	3825	0.83	--	0.03	273	218	3e-57	Unknow 9 	--
rice_2_28804	342	1	145	pep-hit183_Chr6_22499070_22499586_plus	20518	3825	3680	0.83	--	0	146	123	1e-28	Unknow 9 	--

Output:
rice_1_113676	pep-hit15_Chr1_20275998_20276504_minus	247	5	201	20508	11702	11506	0.96	197	247	142	243	20508	11601	11702	0.96	102
rice_2_103300	pep-hit222_Chr7_23268644_23269072_minus	414	1	53	20430	1754	1702	0.96	53	414	362	414	20430	1702	1754	0.96	53


    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 60 --lines 2 --interval 120 --task 1 --mem 15G --time 100:00:00 --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

def pick_highest_match(match_list):
    top_match = [0,0,0,0,0,0,0,0]
    for match in match_list:
        if match[6] > top_match[6]:
            top_match = match
    return top_match

#Query_id        Query_length    Query_start     Query_end       Subject_id      Subject_length  Subject_start   Subject_end     Identity        Positive        Gap     Align_length    Score   E_value Query_annotation
#rice_2_28804    342     78      341     pep-hit183_Chr6_22499070_22499586_plus  20518   3554    3825    0.83
def Paring_MITE_Auto_From_BLAST(infile):
    data = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : list())))
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Query_id'): 
                unit = re.split(r'\t',line)
                #identify > 95% and match length > 50bp
                if float(unit[8]) >= 0.95 and int(unit[11]) >= 50:
                    #query start have match between 1-50 bp 
                    if int(unit[2]) <= 5 and int(unit[3]) >= 50:
                        data[unit[0]][unit[4]]['start'].append([int(unit[1]), int(unit[2]), int(unit[3]), int(unit[5]), int(unit[6]), int(unit[7]), float(unit[8]), int(unit[11])])
                    #query end have match between TElen-50 to TElen
                    elif int(unit[2]) <= int(unit[1]) - 50 and int(unit[3]) >= int(unit[1]) - 5:
                        data[unit[0]][unit[4]]['end'].append([int(unit[1]), int(unit[2]), int(unit[3]), int(unit[5]), int(unit[6]), int(unit[7]), float(unit[8]), int(unit[11])])
    ofile_list = open('%s.pairs.list' %(infile), 'w')
    print >> ofile_list, 'MITE\tAutonomous\tQuery_length\tQuery_start\tQuery_end\t\tSubject_length\tSubject_start\tSubject_end\tIdentity\tAlign_length\tQuery_length\tQuery_start\tQuery_end\t\tSubject_length\tSubject_start\tSubject_end\tIdentity\tAlign_length'
    ofile_log  = open('%s.pairs.log' %(infile), 'w')
    for query in sorted(data.keys()):
        #print query
        for target in sorted(data[query].keys()):
            #print target
            #have both qualified matches from start and end of query.
            if len(data[query][target].keys()) == 2:
                print >> ofile_log, '>%s, %s' %(query, target)
                print >> ofile_log, data[query][target]['start']
                print >> ofile_log, data[query][target]['end']
                #five_end  = [0,0,0,0,0,0,0,0]
                #three_end = [0,0,0,0,0,0,0,0]
                #if len(data[query][target]['start']) == 1:
                #    print 'mark start'
                #    five_end = data[query][target]['start']
                #else:
                #    five_end = pick_highest_match(data[query][target]['start'])
                #if len(data[query][target]['end']) == 1:
                #    print 'mark end'
                #    three_end = data[query][target]['end']
                #else:
                #    three_end = pick_highest_match(data[query][target]['end'])
                five_end = pick_highest_match(data[query][target]['start'])
                three_end = pick_highest_match(data[query][target]['end'])
                #plus to plus match of MITE and autonomous
                if five_end[4] < three_end[5] or five_end[4] < three_end[5]:
                    print >> ofile_log, 'plus to plus'
                    #MITE two ends have match on different ends of autonomous
                    distance = min(three_end[4], three_end[5]) - max(five_end[4], five_end[5])
                    print >> ofile_log, distance
                    if min(three_end[4], three_end[5]) - max(five_end[4], five_end[5]) >= 3000:   
                        print >> ofile_log, '%s\t%s\t%s\t%s\tPairs' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                        print >> ofile_list, '%s\t%s\t%s\t%s\tPairs' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                    else:
                        print >> ofile_log, '%s\t%s\t%s\t%s\tMatch in flanking sequence' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                        #print >> ofile_list, '%s\t%s\t%s\t%s\tMatch in flanking sequence' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                elif five_end[4] > three_end[4] or five_end[5] > three_end[5]:
                    print >> ofile_log, 'plus to minus'
                    distance = min(five_end[4], five_end[5]) - max(three_end[4], three_end[5])
                    print >> ofile_log, distance
                    if min(five_end[4], five_end[5]) - max(three_end[4], three_end[5]) >= 3000:
                        print >> ofile_log, '%s\t%s\t%s\t%s\tPairs' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                        print >> ofile_list, '%s\t%s\t%s\t%s\tPairs' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                    else:
                        print >> ofile_log, '%s\t%s\t%s\t%s\tMatch in flanking sequence' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                        #print >> ofile_list, '%s\t%s\t%s\t%s\tMatch in flanking sequence' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                else:
                    #print 'mark3'
                    print >> ofile_log, '%s\t%s\t%s\t%s\ttMatch in flanking sequence' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))
                    #print >> ofile_list, '%s\t%s\t%s\t%s\tMatch in flanking sequence' %(query, target, '\t'.join(map(str, five_end)), '\t'.join(map(str, three_end)))

    ofile_list.close()
    ofile_log.close()
    return data


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

    Paring_MITE_Auto_From_BLAST(args.input)

if __name__ == '__main__':
    main()

