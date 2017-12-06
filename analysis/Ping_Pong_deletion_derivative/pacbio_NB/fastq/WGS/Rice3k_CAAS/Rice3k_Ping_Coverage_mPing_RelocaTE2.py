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
    #cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 100 --lines %s --interval 120 --resource nodes=1:ppn=1,walltime=200:00:00,mem=10G --convert no %s' %(lines, script)
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 100 --lines %s --interval 120 --task 1 --mem 15G --time 10:00:00 --convert no --queue stajichlab %s' %(lines, script)
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
                if unit[0] == 'mPing' and int(unit[1]) >= 1 and int(unit[1]) <= 430:
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

'''
B001	ERS470219
B002	ERS470220
'''
def readtable(infile):
    data = defaultdict(lambda : str())
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit = re.split(r'\t',line)
                data[unit[0]] = unit[1]
    return data

def ping_coverage_3k(infile):
    acc2name = readtable('/rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/rice_name_acc.list')
    ofile = open('mping_coverage.sh', 'w')
    count = 0
    samtools = '/opt/linux/centos/7.x/x86_64/pkgs/samtools/1.3/bin/samtools'
    bamtools = '/opt/linux/centos/7.x/x86_64/pkgs/bamtools/2.4.0/bin/bamtools'
    bedtools = '/rhome/cjinfeng/BigData/software/bedtools2-2.19.0/bin/bedtools'
    bedping  = '/rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/analysis/Ping_Pong_deletion_derivative/pacbio_NB/fastq/WGS/Rice3k_CAAS/genome.mping_element.bed'
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2 and not line.startswith(r'Taxa'):
                unit = re.split(r'\t',line)
                acc = acc2name[unit[0]]
                bam = '/rhome/cjinfeng/Rice/Rice_population_sequence/Rice_3000/Manuscript/figure/Figure_Ping_SNP/Rice3k_3000_RelocaTEi_mPing_NM2/{}.NM2.bam'.format(acc)
                #bam = 'http://s3.amazonaws.com/3kricegenome/Nipponbare/%s.realigned.bam' %(acc)
                coverage  = 'ping_coverage_3k/%s.mping.coverage.txt' %(unit[0])
                coveragez = 'ping_coverage_3k/%s.mping.coverage.txt.gz' %(unit[0])
                coverage1 = 'ping_coverage_3k/%s.mping.coverage.clean.txt' %(unit[0])
                if not os.path.exists(bam) or int(os.path.getsize(bam)) == 0:
                    print 'Bam file not exists: {}'.format(acc)
                    continue
                if not os.path.exists(coverage1) or int(os.path.getsize(coverage1)) == 0:
                    #bedtools coverage -a test.bed -b genome.ping.bed -d
                    cmd = '''%s view -b %s | %s view -h | awk '/^@|NM:i:0|NM:i:1|NM:i:2/' | %s view -b | %s coverage -abam stdin -b %s -d | awk '{print $1"\\t"$2+$4"\\t"$5}' > %s''' %(samtools, bam, samtools, samtools, bedtools, bedping, os.path.abspath(coverage1))
                    #cmd = '%s view -b %s chr06 | %s filter -tag NM:0 -tag NM:1 | %s genomecov -ibam stdin -d > %s' %(samtools, bam, bamtools, bedtools, os.path.abspath(coverage))
                    #cmd = '%s view -b %s chr06:23520641-23527981 | %s filter -tag NM:0 -tag NM:1 | %s genomecov -ibam stdin -d -g %s > %s' %(samtools, bam, bamtools, bedtools, bedping, os.path.abspath(coverage))
                    #cmd = '%s view -b %s chr06 | %s genomecov -ibam stdin -d > %s' %(samtools, bam, bedtools, os.path.abspath(coverage))
                    #gz  = '/usr/bin/pigz %s -p 1 -f' %(os.path.abspath(coverage))
                    #sed = 'zcat %s | awk -F"\\t" \'$2>23520641 && $2<23527981\' > %s' %(os.path.abspath(coveragez), os.path.abspath(coverage1))
                    print >> ofile, cmd
                    #print >> ofile, gz
                    #print >> ofile, sed
                    count += 1
    ofile.close()
    if count > 0:
        runjob('mping_coverage.sh', 100)
   
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

    #####summarize coverage into matrix

    covs = glob.glob('%s/*.mping.coverage.clean.txt' %('ping_coverage_3k'))
    all_num = defaultdict(lambda : int())
    all_line= defaultdict(lambda : list())
    for cov in covs:
        name = os.path.split(cov)[1] 
        cov_num, cov_line = read_cov(cov)
        all_num[name]  = cov_num
        all_line[name] = cov_line
        print name, cov_num
    ofile = open(args.output, 'w')
    ofile1 = open('%s.header' %(args.output), 'w') 
    for name, num in sorted(all_num.items(), key=lambda x:x[1]):
        print >> ofile1, '%s\t%s\t%s' %(name, num, '\t'.join(all_line[name]))
        print >> ofile, '\t'.join(all_line[name])
    ofile.close()


if __name__ == '__main__':
    main()

