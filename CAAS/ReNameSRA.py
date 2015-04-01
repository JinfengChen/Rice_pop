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
python ReNameSRA.py > acc2strain.list 2> log2 &

--mode: dump or gzip
    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/software/bin/qsub-pbs.pl --maxjob 30 --lines %s --interval 120 --resource walltime=100:00:00,mem=5G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

#ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByStudy/sra/SRP/SRP003/SRP003189/
#"SRX025294","Resequencing of 50 rice individuals-rufipogon_Yuan3-9 ","Oryza sativa","Illumina Genome Analyzer II","BGI","SRP003189","Resequencing of 50 rice individuals","SRS086373","","243.58","1","6711790","590637520","ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/SRX/SRX025/SRX025294","SZC08001CTDCAAPE","WGS","GENOMIC","PCR"
def read_sra_inf(infile):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit    = re.split(r',', line)
                acc     = re.sub(r'"','', unit[0])
                strain  = re.sub(r'"','', unit[1][37:])
                strain  = re.sub(r' ','', strain)
                link    = re.sub(r'"','', unit[13])
                link    = re.sub(r' ','', link)
                data[acc] = [strain, link]
    return data


#SRR063622,2011-12-15 10:40:33,2011-12-15 10:40:33,33451859,6690371800,33451859,200,3134,,ftp://ftp-trace.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR063/SRR063622/SRR063622.sra,SRX025244
def read_sra_run(infile, sra2strain):
    data = defaultdict(str)
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit    = re.split(r',', line)
                acc     = unit[0]
                run     = unit[10]
                if sra2strain.has_key(run):
                    #print acc, sra2strain[run]
                    data[acc] = sra2strain[run]
    return data




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode')
    parser.add_argument('-o', '--output')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    #try:
    #    len(args.input) > 0
    #except:
    #    usage()
    #    sys.exit(2)
    
    if args.mode is None:
        args.mode = 'dump'
    sra2strain = read_sra_inf('sra_result.csv')
    acc2strain = read_sra_run('SraRunInfo.csv', sra2strain)   

    if not os.path.exists('fastq'):
        os.mkdir('fastq')
    outdir = os.path.abspath('./fastq')
    sras = glob.glob('SRP003189/*/*.sra')
    ofile = open('dump.sh', 'w')
    for sra in sras:
        acc    = os.path.split(os.path.splitext(sra)[0])[-1]
        #acc = os.path.splitext(sra)[0]
        print acc, acc2strain[acc][0]
        subdir = os.path.abspath('./fastq/%s' %(acc2strain[acc][0]))
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        sra_cp = '%s/%s/%s_%s.sra' %(outdir, acc2strain[acc][0], acc, acc2strain[acc][0])
        if not os.path.isfile(sra_cp):
            os.system('ln -s %s %s' %(os.path.abspath(sra), sra_cp))
        fq1    = '%s/%s/%s_%s_1.fastq' %(outdir, acc2strain[acc][0], acc, acc2strain[acc][0])
        fq2    = '%s/%s/%s_%s_2.fastq' %(outdir, acc2strain[acc][0], acc, acc2strain[acc][0])
        fq1gz  = '%s/%s/%s_%s_1.fastq.gz' %(outdir, acc2strain[acc][0], acc, acc2strain[acc][0])
        fq2gz  = '%s/%s/%s_%s_2.fastq.gz' %(outdir, acc2strain[acc][0], acc, acc2strain[acc][0])
        cmd    = []
        if not os.path.isfile(fq1) and not os.path.isfile(fq1gz) and args.mode == 'dump':
            #do dump and gzip
            cmd.append('/opt/sratoolkit/2.4.2/bin/fastq-dump --outdir %s --split-files %s' %(subdir, sra_cp))
            cmd.append('gzip %s' %(fq1))
            cmd.append('gzip %s' %(fq2))
            #pass
        elif os.path.isfile(fq1) and not os.path.isfile(fq1gz) and args.mode == 'gzip':
            #do gzip only
            cmd.append('gzip %s' %(fq1))
            cmd.append('gzip %s' %(fq2))
        for c in cmd:
            if not c == '':
                print >> ofile, c
    ofile.close()

    if args.mode == 'dump':
        #do dump and gzip
        runjob('dump.sh', 3)
    else:
        #do gzip only
        runjob('dump.sh', 1)

if __name__ == '__main__':
    main()

