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
python Ping_matrix.py --input Ping_Indenesia_group.list,Ping_SouthKorea_group.list --gff Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.gff


    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource nodes=1:ppn=12,walltime=100:00:00,mem=20G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)



def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid

#Ping_Indenesia_group.list
#ERS467891_RelocaTEi     3       3       0       IRIS313-9301    Indonesia       Tropical japonica
def read_strain_inf(infile):
    data = defaultdict(lambda : list())
    strain_ordered = defaultdict(lambda : list())
    group= re.split(r'_', os.path.split(infile)[1])[1]
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Acc'): 
                unit = re.split(r'\t',line)
                unit[5]= group
                strain = re.sub(r'_RelocaTEi', r'', unit[0])
                strain_ordered[group].append(strain)
                data[strain] = unit
    return data, group, strain_ordered

def split_strain_groups(in_dict):
    strain_groups  = defaultdict(lambda : list())
    for strain in sorted(in_dict.keys()):
        strain_groups[in_dict[strain][5]].append(strain)
    return strain_groups

#Chr7    ERS470003       RelocaTE_i      14635489        14635491        .       -       .       ID
def read_gff(infile, strain_inf):
    data = defaultdict(lambda : defaultdict(lambda : int()))
    ping_list = defaultdict(lambda : int())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                strain = unit[1]
                ping   = '%s:%s' %(unit[0], unit[3])
                if strain_inf.has_key(strain):
                    data[strain][ping] = 1
                    ping_list[ping]
    return data, ping_list.keys()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-g', '--gff')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        len(args.input) > 0
    except:
        usage()
        sys.exit(2)

    if not args.output:
        args.output = 'Ping_spread_matirx'    
  
    strain_inf     = defaultdict(lambda : list())
    strain_groups  = defaultdict(lambda : list())

    #read in strain for analysis
    groups = []
    #strain_ordered = defaultdict(lambda : list())
    strain_list = re.split(r',', args.input)
    for strain in strain_list:
        strain_inf.update
        inf, group_temp, order_temp = read_strain_inf(strain)
        strain_inf.update(inf)
        strain_groups.update(order_temp)
        groups.append(group_temp)

    #split strains into difference group based on origin, indonesisa or south koran
    #strain_groups = split_strain_groups(strain_inf)

    #read in gff
    strain_ping_dict, ping_list = read_gff(args.gff, strain_inf)
  
    print 'Number of strain: %s' %(len(strain_inf.keys()))
    print 'Number of ping: %s' %(len(ping_list))
 
    #output matirx
    ofile = open('%s.matrix' %(args.output), 'w')
    print >> ofile, 'Strain\t%s' %('\t'.join(sorted(ping_list)))
    #for group in ['Indonesia', 'SouthKorea', 'Landrace']:
    for group in groups:
        ofile1 = open('%s_%s.matrix' %(args.output, re.sub(r' ', r'', group)), 'a')
        print >> ofile1, 'Strain\t%s' %('\t'.join(sorted(ping_list)))
        for strain in strain_groups[group]:
            strain_row = [strain_inf[strain][4]] 
            for ping in sorted(ping_list):
                if strain_ping_dict[strain][ping] == 1:
                    strain_row.append(1)
                else:
                    strain_row.append(0)
            print >> ofile, '\t'.join(map(str, strain_row))
            print >> ofile1, '\t'.join(map(str, strain_row))
        ofile1.close()
    ofile.close()

if __name__ == '__main__':
    main()

