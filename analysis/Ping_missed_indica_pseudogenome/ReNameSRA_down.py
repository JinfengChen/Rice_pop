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
python ReNameSRA_down.py

    '''
    print message

def fasta_id(fastafile):
    fastaid = defaultdict(str)
    for record in SeqIO.parse(fastafile,"fasta"):
        fastaid[record.id] = 1
    return fastaid


def runjob(script, lines):
    cmd = 'perl /rhome/cjinfeng/BigData/software/bin/qsub-slurm.pl --maxjob 30 --lines %s --interval 120 --task 1 --mem 5G --time 20:00:00 --convert no %s' %(lines, script)
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

#1       B001    China   Temperate japonica      ERS470219       ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/ERR/ERR622/ERR622583/ERR622583.sra
#1       B001    China   Temperate japonica      ERS470219       ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/ERR/ERR622/ERR622584/ERR622584.sra
def read_link(infile, outdir):
    data  = defaultdict(str)
    ofile = open('down.sh', 'a')
    with open (infile, 'r') as filehd:
        for line in filehd:
            line = line.rstrip()
            if len(line) > 2: 
                unit    = re.split(r'\t', line)
                acc     = os.path.abspath('%s/%s' %(outdir, unit[4]))
                link    = unit[5]
                sra     = '%s/%s' %(acc, os.path.split(link)[1])
                sra_temp= '%s.aspx' %(sra)
                fq      = re.sub(r'.sra', r'_1.fastq.gz', sra)
                if not os.path.exists(acc):
                    os.mkdir(acc)
                if os.path.isfile(sra) and os.path.isfile(sra_temp):
                    os.system('rm %s %s' %(sra, sra_temp))
                    cmd     = '/opt/linux/centos/7.x/x86_64/pkgs/aspera/3.3.3/bin/ascp -i /opt/linux/centos/7.x/x86_64/pkgs/aspera/3.3.3/etc/asperaweb_id_dsa.openssh -k 1 -T -l20m %s %s' %(link, acc)
                    print >> ofile, cmd
                elif not os.path.isfile(sra) and not os.path.isfile(fq):
                    cmd     = '/opt/linux/centos/7.x/x86_64/pkgs/aspera/3.3.3/bin/ascp -i /opt/linux/centos/7.x/x86_64/pkgs/aspera/3.3.3/etc/asperaweb_id_dsa.openssh -k 1 -T -l20m %s %s' %(link, acc)
                    print >> ofile, cmd
                    #print >> ofile, sra
    ofile.close()
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
    if not args.output:
        args.output = 'IRRI_mPing'
    outdir = args.output
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    os.system('rm down.sh')

    #read_link('temperate.mPing.group.id.download.list', outdir)
    #read_link('temperate.mPing.group.id.other0.download.list', outdir)
    #read_link('temperate.mPing.group.id.other1.download.list', outdir)
    #read_link('temperate.mPing.group.id.other2.download.list', outdir)
    #read_link('temperate.mPing.group.id.other3.download.list', outdir)
    #read_link('temperate.mPing.group.id.other4.download.list', outdir)
    #read_link('temperate.mPing.group.id.other5.download.list', outdir)
    #read_link('temperate.mPing.group.id.other6.download.list', outdir)

    #non japonica strains
    #read_link('rice_line_IRRI_2466.other0.download.list', outdir)
    #read_link('rice_line_IRRI_2466.other1.download.list', outdir)
    #read_link('rice_line_IRRI_2466.other2.download.list', outdir)
    #read_link('rice_line_IRRI_2466.other3.download.list', outdir)
    #read_link('rice_line_IRRI_2466.other4.download.list', outdir)
    #read_link('rice_line_IRRI_2466.other5.download.list', outdir)
    #read_link('rice_line_IRRI_2466.other6.download.list', outdir)
    #read_link('rice_line_IRRI_2466.other7.download.list', outdir)
    #read_link('rice_line_IRRI_2466.other8.download.list', outdir)
    #japonica strains
    #read_link('rice_line_IRRI_2466.Japonica9.download.list', outdir)
    #read_link('rice_line_IRRI_2466.Japonica10.download.list', outdir)
    #read_link('rice_line_IRRI_2466.Japonica11.download.list', outdir)
    #read_link('rice_line_IRRI_2466.Japonica12.download.list', outdir)
    
    #read_link('rice_line_IRRI_2466.download.HEG4_group.list', outdir)
    #read_link('rice_line_IRRI_2466.download.HEG4_temperate.list', outdir)

    #read_link('stowaway_check_candidate_fq.status.insertion.list.download.list', outdir)
    #read_link('Ping_test.list.download.list', outdir)
    read_link('RelocaTE2_Depth_Ping2.txt.download.list', outdir)

    #runjob('down.sh', 100) #more than 1000 jobs
    runjob('down.sh', 2) #more than 1000 jobs
    #runjob('down.sh', 5) #100 jobs
    #runjob('down.sh', 2) #30 jobs
    
if __name__ == '__main__':
    main()

