echo "list of strains have stowaway element"
ln -s ../Stowaway_element/stowaway_check_candidate_fq.status.insertion.list ./
echo "stowaway with ping insertion"
ln -s ../Stowaway_element/stowaway.fasta ./
ln -s ../Stowaway_element/stowaway.insertion.list ./
ln -s ../Stowaway_element/stowaway.flank1k.fa ./
cp ~/BigData/00.RD/RelocaTE_i/Simulation/Reference/ping.fa ./
python mPing_flank.py --genome stowaway.flank1k.fa --list ping.insertion.list --fasta ping.fa --output stowaway.flank1k.ping.fa

echo "download fq for strains have stowaway element"
python ReNameSRA_subset.py --input stowaway_check_candidate_fq.status.insertion.list
#199 strains
cut -f2 stowaway_check_candidate_fq.status.insertion.list.download.list | uniq | sort | uniq | wc -l
#1712 job
stowaway_check_candidate_fq.status.insertion.list.download.list
python ReNameSRA_down.py --output 3k_stowaway_strains > log 2>&1 &
python ReNameSRA_merge.py --input 3k_stowaway_strains/ > log 2>&1 &

echo "run mapping"
python Run_Merge_multi_sample.py --fastq_dir test_fq/ > log 2>&1 &
python Run_Merge_multi_sample.py --fastq_dir 3k_stowaway_strains/ > log 2>&1 &
python Run_Map_multi_sample.py --fastq_dir test_fq/ --genome stowaway.flank1k.fa > log 2>&1 &
python Run_Map_multi_sample.py --fastq_dir 3k_stowaway_strains/ --genome stowaway.flank1k.ping.fa > log 2>&1 &


