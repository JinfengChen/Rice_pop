#harbinger
module load ncbi-blast/2.2.26
formatdb -i nonredundant_pep_union-10kb.fa -p F
blastall -p blastn -i MSU7.MITEhunter.fasta.len800.fasta -d nonredundant_pep_union-10kb.fa -o MITE2Auto.blast
perl ~/BigData/software/bin/blast_parser.pl MITE2Auto.blast > MITE2Auto.blast.table
python MITE_Auto_Pairs.py --input MITE2Auto.blast.table

#marine
formatdb -i Mariner.fa -p F
blastall -p blastn -i MSU7.MITEhunter.fasta.len800.fasta -d Mariner.fa -o MITE2mariner.blast
perl ~/BigData/software/bin/blast_parser.pl MITE2mariner.blast > MITE2mariner.blast.table
python MITE_Auto_Pairs.py --input MITE2mariner.blast.table

#mutator
formatdb -i Mutator.fa -p F
blastall -p blastn -i MSU7.MITEhunter.fasta.len800.fasta -d Mutator.fa -o MITE2mutator.blast
perl ~/BigData/software/bin/blast_parser.pl MITE2mutator.blast > MITE2mutator.blast.table
python MITE_Auto_Pairs.py --input MITE2mutator.blast.table

#hAT
formatdb -i hAT.fa -p F
blastall -p blastn -i MSU7.MITEhunter.fasta.len800.fasta -d hAT.fa -o MITE2hAT.blast
perl ~/BigData/software/bin/blast_parser.pl MITE2hAT.blast > MITE2hAT.blast.table
python MITE_Auto_Pairs.py --input MITE2hAT.blast.table

echo "pipeline"
bash Blast_MITE2Auto.sh
python Blast_MITE2Auto_sum.py --input ./

