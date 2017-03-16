blastall -p blastn -i MSU7.MITEhunter.fasta.len800.fasta -d nonredundant_pep_union-10kb.fa -o MITE2Auto.blast
perl ~/BigData/software/bin/blast_parser.pl MITE2Auto.blast > MITE2Auto.blast.table
python MITE_Auto_Pairs.py --input MITE2Auto.blast.table

