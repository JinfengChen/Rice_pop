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
                #$2>29071995 && $2<29077870
                if unit[0] == 'chr03' and int(unit[1]) >= 29077870 and int(unit[1]) <= 29077870:
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


def ping_coverage_3k(infile):
    ofile = open('actin_coverage.sh', 'w')
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
                local_bam = 'ping_coverage_3k/%s.realigned.bam' %(acc)
                coverage  = 'ping_coverage_3k/%s.actin.coverage.txt' %(acc)
                coveragez = 'ping_coverage_3k/%s.actin.coverage.txt.gz' %(acc)
                coverage1 = 'ping_coverage_3k/%s.actin.coverage.clean.txt' %(acc)
                if not os.path.exists(coverage1) or int(os.path.getsize(coverage1)) == 0:
                #if os.path.exists(local_bam) and int(os.path.getsize(coverage1)) == 0:
                    down= 'wget %s -O %s' %(bam, os.path.abspath(local_bam))
                    index = '%s index %s' %(samtools, os.path.abspath(local_bam))
                    cmd = '%s view -b %s chr03 | %s genomecov -ibam stdin -d > %s' %(samtools, os.path.abspath(local_bam), bedtools, os.path.abspath(coverage))
                    gz  = '/usr/bin/pigz %s -p 1 -f' %(os.path.abspath(coverage))
                    sed = 'zcat %s | awk -F"\\t" \'$2>29071995 && $2<29077870\' > %s' %(os.path.abspath(coveragez), os.path.abspath(coverage1))
                    print >> ofile, down
                    print >> ofile, index
                    print >> ofile, cmd
                    print >> ofile, gz
                    print >> ofile, sed
                    count += 1
    ofile.close()
    if count > 0:
        runjob('actin_coverage.sh', 5)
   
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
    ping_coverage_3k(args.input)
'''
    #####summarize coverage into matrix
    covs = glob.glob('%s/*.ping.coverage.clean.txt' %('ping_coverage_3k'))
    all_num = defaultdict(lambda : int())
    all_line= defaultdict(lambda : list())
    for cov in covs:
        name = os.path.split(cov)[1] 
        cov_num, cov_line = read_cov(cov)
        all_num[name]  = cov_num
        all_line[name] = cov_line
    ofile = open(args.output, 'w')
    ofile1 = open('%s.header' %(args.output), 'w') 
    for name, num in sorted(all_num.items(), key=lambda x:x[1]):
        print >> ofile1, '%s\t%s\t%s' %(name, num, '\t'.join(all_line[name]))
        print >> ofile, '\t'.join(all_line[name])
    ofile.close()
'''
if __name__ == '__main__':
    main()

