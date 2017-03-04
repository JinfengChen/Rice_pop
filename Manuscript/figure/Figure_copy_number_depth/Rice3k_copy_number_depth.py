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
import subprocess

def usage():
    test="name"
    message='''
python Rice3k_copy_number_depth.py > log 2>&1 &

    '''
    print message


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-pbs.pl --maxjob 100 --lines %s --interval 120 --resource nodes=1:ppn=1,walltime=200:00:00,mem=10G --convert no %s' %(lines, script)
    #print cmd 
    os.system(cmd)

#SN      insert size average:    464.1
#SN      insert size standard deviation: 45.7
#SN      bases mapped:   15136373269     # ignores clipping
def read_cov(infile):
    size = 0.0
    sd   = 0.0
    #r = re.compile(r'(\d+)')
    #print infile
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if 'insert size average:' in line:
                unit = re.split(r'\s+', line)
                #print line
                #print unit[3]
                size = unit[4]
            elif 'insert size standard deviation:' in line:
                unit = re.split(r'\s+', line)
                #print line
                #print unit[3]
                sd = unit[5]
    
    return size, sd

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
    #try:
    #    len(args.input) > 0
    #except:
    #    usage()
    #    sys.exit(2)
    
    if not args.output:
        args.output = 'ping_coverage_rice3000_MSU7.matrix'
 
    #test_bam(args.input)
    #read_depth_3k(args.input)

    #####summarize coverage into matrix
    covs = glob.glob('%s/*.pong.coverage.clean.txt' %('ping_coverage_3k'))
    ofile = open('rice_3k_copy_number_depth.txt', 'w')
    print >> ofile, "Taxa\tPingDepth\tPingCopyNumber\tPongDepth\tPongCopyNumber\tActinDepth"
    for pong in covs:
        name  = os.path.split(pong)[1]
        name  = re.sub(r'\.pong\.coverage\.clean\.txt', r'', name) 
        ping  = '%s.ping.coverage.clean.txt' %(name)
        actin = '%s.actin.coverage.clean.txt' %(name) 
        #head -n 6164 ping_coverage_3k/B160.pong.coverage.clean.txt | tail -n 5164 |cut -f3 | perl ~/BigData/software/bin/numberStat.pl
        #pong_cmd = 'head -n 6164 ping_coverage_3k/%s.pong.coverage.clean.txt | tail -n 5164 |cut -f3 | perl ~/BigData/software/bin/numberStat.pl | grep "mean value" | sed "s/mean value://" | sed "s/ //g"' %(name)
        pong_cmd = 'head -n 5964 ping_coverage_3k/%s.pong.coverage.clean.txt | tail -n 4964 |cut -f3 | perl ~/BigData/software/bin/numberStat.pl | grep "mean value" | sed "s/mean value://" | sed "s/ //g"' %(name)
        pong_avg = subprocess.Popen(pong_cmd, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
        #ping_cmd = 'head -n 6339 ping_coverage_3k/%s.ping.coverage.clean.txt | tail -n 5339 |cut -f3 | perl ~/BigData/software/bin/numberStat.pl | grep "mean value" | sed "s/mean value://" | sed "s/ //g"' %(name)
        ping_cmd = 'head -n 6139 ping_coverage_3k/%s.ping.coverage.clean.txt | tail -n 5139 |cut -f3 | perl ~/BigData/software/bin/numberStat.pl | grep "mean value" | sed "s/mean value://" | sed "s/ //g"' %(name)
        ping_avg = subprocess.Popen(ping_cmd, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
        act_cmd = 'head -n 4874 ping_coverage_3k/%s.actin.coverage.clean.txt | tail -n 3874 |cut -f3 | perl ~/BigData/software/bin/numberStat.pl | grep "mean value" | sed "s/mean value://" | sed "s/ //g"' %(name)
        act_avg = subprocess.Popen(act_cmd, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
        #print >> ofile, '%s\t%s\t%s\t%s' %(name, ping_avg, pong_avg, act_avg)
        #num = subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
        ping_cp = str(float(ping_avg)/float(act_avg))
        pong_cp = str(float(pong_avg)*6/float(act_avg))
        print >> ofile, '%s\t%s\t%s\t%s\t%s\t%s' %(name, ping_avg, ping_cp, pong_avg, pong_cp, act_avg)
    ofile.close()

if __name__ == '__main__':
    main()

