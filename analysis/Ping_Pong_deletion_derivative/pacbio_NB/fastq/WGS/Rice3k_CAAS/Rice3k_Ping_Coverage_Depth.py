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


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 100 --lines %s --interval 120 --resource nodes=1:ppn=1,walltime=200:00:00,mem=10G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

#SN      bases mapped:   15136373269     # ignores clipping
def read_cov(infile):
    depth = 0.0
    #r = re.compile(r'(\d+)')
    #print infile
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if 'bases mapped:' in line:
                unit = re.split(r'\s+', line)
                #print line
                #print unit[3]
                base = unit[3]
            elif 'average length:' in line:
                unit = re.split(r'\s+', line)
                #print line
                #print unit[3]
                length = unit[3]
    depth = float(base)/372000000
    return depth

#samtools view http://s3.amazonaws.com/3kricegenome/Nipponbare/IRIS_313-10271.realigned.bam
def ping_coverage(acc):
    #cmd = '/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools view http://s3.amazonaws.com/3kricegenome/Nipponbare/%s.realigned.bam > test.sam' %(acc)
    bam = 'http://s3.amazonaws.com/3kricegenome/Nipponbare/%s.realigned.bam' %(acc)
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


def read_depth_3k(infile):
    ofile = open('rice_3k_depth.sh', 'w')
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
                stats  = 'ping_coverage_3k/%s.stats.txt' %(acc)
                if not os.path.exists(stats):
                    cmd = '%s stats %s > %s' %(samtools, bam, os.path.abspath(stats))
                    print >> ofile, cmd
                    count += 1
    ofile.close()
    if count > 0:
        runjob('rice_3k_depth.sh', 5)
   
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
    
    if not args.output:
        args.output = 'ping_coverage_rice3000_MSU7.matrix'
 
    #test_bam(args.input)
    read_depth_3k(args.input)

    #####summarize coverage into matrix
    covs = glob.glob('%s/*.stats.txt' %('ping_coverage_3k'))
    ofile = open('rice_3k_depth.txt', 'w')
    for cov in covs:
        name  = os.path.split(cov)[1]
        name  = re.sub(r'\.stats\.txt', r'', name) 
        depth = read_cov(cov)
        print >> ofile, '%s\t%s' %(name, depth)
    ofile.close()

if __name__ == '__main__':
    main()

