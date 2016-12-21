#!/bin/bash
#PBS -l nodes=1:ppn=1
#PBS -l mem=2gb
#PBS -l walltime=100:00:00
#PBS -j oe
#PBS -V
#PBS -d ./

#cd $PBS_O_WORKDIR


start=`date +%s`

wget http://s3.amazonaws.com/3kricegenome/Nipponbare/IRIS_313-11800.realigned.bam
wget http://s3.amazonaws.com/3kricegenome/Nipponbare/IRIS_313-11651.realigned.bam

end=`date +%s`
runtime=$((end-start))

echo "Start: $start"
echo "End: $end"
echo "Run time: $runtime"

echo "Done"

