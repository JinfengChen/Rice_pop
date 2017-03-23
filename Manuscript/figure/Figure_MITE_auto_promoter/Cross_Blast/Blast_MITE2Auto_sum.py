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
python CircosConf.py --input circos.config --output pipe.conf

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

#rice_1_100587   RepeatMasker    Transposon      1       342     1074    +       .       ID=TE001;Target=CASTAWAY 8 360;Class=DNA/PIF-Harbinger;PercDiv
def parse_MITE_repeatmasker(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'#'): 
                unit = re.split(r'\t',line)
                repeat = unit[0]
                attrs = re.split(r';', unit[8])
                temp = defaultdict(lambda : str())
                for attr in attrs:
                    if not attr == '':
                        idx, value = re.split(r'\=', attr)
                        temp[idx] = value
                repname = re.split(r' ', temp['Target'])[0]
                repfam  = temp['Class']
                data[repeat] = '%s : %s' %(repname, repfam)
    return data

#Target_Dirs     Query   QueryLength     NumberOfSequence        Avg_Identity    AvgAlignLength
#Target/Target_Run_MITE_MSU7_2017_03_19_154911/MSU7.MITEhunter.fasta.len800_split1       rice_2_28804_Unknow_9   342     48      0.901727286012  323.0
def parse_MITE_copy_identity(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Target_Dirs'): 
                unit = re.split(r'\t',line)
                temp = re.split(r'_', unit[1])
                repeat = '_'.join(temp[:3])
                data[repeat] = line
    return data

#MITE    Autonomous      Query_length    Query_start     Query_end               Subject_length  Subject_start   Subject_end     Identity        Align_length    Query_length    Query_start     Query_end       
#rice_1_33417    pep-hit27_HG417165.1_21310446_21311048_minus    510     8       198     20604   12893   12703   0.92    191     510     190     510     20604   7808    7491    0.92    321     Pairs
def parse_file(infile, strain, repeat, mite2auto):
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'MITE'):
                unit = re.split(r'\t',line)
                mite2auto[unit[0]][strain].append('%s:%s' %(unit[1], repeat))


def mite2auto_strain_sum(mite2auto, MITE_info):
    mite2auto_strain = defaultdict(lambda : list())   
    strains = ['MSU7', 'OID_1', 'DJ123', 'IR64', 'ONI_1', 'ORU_1', 'ORU_Australia', 'ORU_W1943', 'OGL', 'OBA', 'OME_1', 'OLO', 'OGU_1', 'OPU', 'OBR']
    for repeat in sorted(MITE_info.keys()):
        if mite2auto.has_key(repeat):
            for strain in strains:
                if mite2auto[repeat].has_key(strain):
                    mite2auto_strain[repeat].append(';'.join(mite2auto[repeat][strain]))
                else:
                    mite2auto_strain[repeat].append('NA')
        else:
            for strain in strains:
                mite2auto_strain[repeat].append('NA')
    return mite2auto_strain

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

    MITE_info = parse_MITE_copy_identity('Target_Run_MITE_MSU7_2017_03_19_154911.MITE_copy_identify.brief.txt') 
    MITE_anno = parse_MITE_repeatmasker('MSU7.MITEhunter.fasta.len800.fasta.out.gff')
    #MITE2ORU_W1943_mutator.blast.table.pairs.0.9_50_10.list
    sumfiles = glob.glob('%s/*.blast.table.pairs.0.9_50_10.list' %(args.input))
    r = re.compile(r'MITE2(.*)_(\w+)\.blast\.table\.pairs')
    mite2auto = defaultdict(lambda : defaultdict(lambda : list())) # repeat -> strain -> [element:family, element:family]
    for f in sorted(sumfiles):
        m = r.search(f)
        strain = 'NA'
        repeat = 'NA'
        if m:
            strain = m.groups(0)[0]
            repeat = m.groups(0)[1]
        parse_file(f, strain, repeat, mite2auto)
        #print f, strain, repeat
    mite2auto_strain = mite2auto_strain_sum(mite2auto, MITE_info)
    ofile = open('temp.sum.txt', 'w')
    print >> ofile, 'Repaet\tTarget_Dirs\tQuery\tQueryLength\tNumberOfSequence\tAvg_Identity\tAvgAlignLength\tRepeat:Family\tMSU7\tOID_1\tDJ123\tIR64\tONI_1\tORU_1\tORU_Australia\tORU_W1943\tOGL\tOBA\tOME_1\tOLO\tOGU_1\tOPU\tOBR'
    for repeat in sorted(MITE_info):
        repeat_anno = MITE_anno[repeat] if MITE_anno.has_key(repeat) else 'NA'
        print >> ofile, '%s\t%s\t%s\t%s' %(repeat, MITE_info[repeat], repeat_anno, '\t'.join(mite2auto_strain[repeat]))
    ofile.close()

if __name__ == '__main__':
    main()

