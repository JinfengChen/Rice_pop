cp test.phy infile
rm outfile
echo y | dnadist
cp outfile test.phy.dist
mv outfile infile
echo y | neighbor
mv outtree test.phy.tree

