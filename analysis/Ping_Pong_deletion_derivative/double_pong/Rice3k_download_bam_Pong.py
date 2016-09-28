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
import urllib2

def usage():
    test="name"
    message='''
python CircosConf.py --input circos.config --output pipe.conf

    '''
    print message

def createdir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 100 --lines %s --interval 120 --resource nodes=1:ppn=1,walltime=20:00:00,mem=10G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)


def read_cov(infile):
    name     = os.path.split(infile)[1]
    coverage = 0
    data     = []
    count   = 0
    covered = 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2:
                flag = 0 
                unit = re.split(r'\t',line)
                #$2>21719706 && $2<21726871
                if unit[0] == 'chr06' and int(unit[1]) >= 21719706 and int(unit[1]) <= 21726871:
                    if int(unit[2]) > 0:
                        data.append('10')
                    else:
                        data.append('0')
                    count += 1
                    if int(unit[2]) > 0:
                        covered += 1
    coverage = covered
    return coverage, data

#samtools view http://s3.amazonaws.com/3kricegenome/Nipponbare/IRIS_313-10271.realigned.bam
def ping_coverage(acc):
    #cmd = '/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view http://s3.amazonaws.com/3kricegenome/Nipponbare/%s.realigned.bam > test.sam' %(acc)
    bam = 'http://s3.amazonaws.com/3kricegenome/Nipponbare/%s.realigned.bam.bai' %(acc)
    file_ok    = 0
    try: 
        urllib2.urlopen(bam)
        file_ok = 1
        print '%s: okay' %(bam)
    except urllib2.HTTPError, e:
        print '%s: %s' %(bam, e.code)
        file_ok = 0
    except urllib2.URLError, e:
        print '%s: %s' %(bam, e.code)
        file_ok = 0
   
    return file_ok 


#Taxa    Color   Label   Name    Origin  Group   mPing   Ping    Pong
#B001    blue    Heibiao|B001|Temp       Heibiao China   Temperate jap   71      1       8
def test_bam(infile):
    file_ok = 0
    file_wrong = 0
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                if not unit[0] == 'Taxa':
                    file_status = ping_coverage(unit[0])
                    if file_status == 0:
                        file_wrong +=1
                    elif file_status == 1:
                        file_ok    += 1
    print 'Okay: %s' %(file_ok)
    print 'Wrong: %s' %(file_wrong)  


def pong_3k(infile):
    ofile = open('pong_fastq.sh', 'w')
    count = 0
    samtools = '/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools'
    bedtools = '/rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools'
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa'):
                unit = re.split(r'\t',line)
                acc = unit[0]
                bam = 'http://s3.amazonaws.com/3kricegenome/Nipponbare/%s.realigned.bam' %(acc)
                #bam = '~/BigData/01.Rice_genomes/A123/00.Bam/A123_MSU7_BWA/A123_0.clean.A123_CLEAN.bam' 
                outdir = os.path.abspath('pong_3k')
                createdir(outdir)
                createdir('%s/%s_pong' %(outdir, acc))
                local_bam = '%s/%s.realigned.bam' %(outdir, acc)
                pong_sam  = '%s/%s.pong.sam' %(outdir, acc)
                pong_bam  = '%s/%s.pong.bam' %(outdir, acc)
                pong_sort_bam  = '%s/%s.pong.byname.bam' %(outdir, acc)
                #local_bam = os.path.abspath(local_bam)
                #pong_bam  = os.path.abspath(pong_bam)
                #pong_sort_bam = os.path.abspath(pong_sort_bam)
                if not os.path.exists(pong_sort_bam) or int(os.path.getsize(pong_sort_bam)) == 0:
                    #print acc
                    #down= 'wget %s -O %s' %(bam, os.path.abspath(local_bam))
                    #index = '%s index %s' %(samtools, os.path.abspath(local_bam))
                    #cmd1 = '%s intersect -abam %s -b %s > %s' %(bedtools, bam, os.path.abspath('Pong_2k.gff'), pong_bam)
                    cmd0 = '%s view -H %s > %s' %(samtools, bam, pong_sam)
                    cmd1 = '%s view %s chr11:11434715-11443880 >> %s' %(samtools, bam, pong_sam)
                    cmd2 = '%s view %s chr02:19902309-19911474 >> %s' %(samtools, bam, pong_sam)
                    cmd3 = '%s view %s chr06:12413640-12427974 >> %s' %(samtools, bam, pong_sam)
                    cmd4 = '%s view %s chr06:21718706-21727871 >> %s' %(samtools, bam, pong_sam)
                    cmd5 = '%s view %s chr09:11300206-11309371 >> %s' %(samtools, bam, pong_sam)
                    cmd6 = '%s view -Sb %s > %s' %(samtools, pong_sam, pong_bam)
                    cmd7 = '%s sort -n %s -o %s' %(samtools, pong_bam, pong_sort_bam)
                    cmd8 = '%s bamtofastq -i %s -fq %s/%s_pong/%s_Pong_1.fq -fq2 %s/%s_pong/%s_Pong_2.fq' %(bedtools, pong_sort_bam, outdir, acc ,acc, outdir, acc, acc) 
                    print >> ofile, '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' %(cmd0, cmd1, cmd2, cmd3, cmd4, cmd5, cmd6, cmd7, cmd8)
                    count += 1
    ofile.close()
    if count > 0:
        runjob('pong_fastq.sh', 9)
   
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
    
 
    #test_bam(args.input)
    pong_3k(args.input)

if __name__ == '__main__':
    main()

