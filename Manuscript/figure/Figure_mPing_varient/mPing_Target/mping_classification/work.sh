echo "copy Target result"
cp -R ../Target/Target_Run_mPing_rice3k.fa.* ./
echo "clean flanking sequence and N in mPing element"
python Extract_mPing_varients.py --input rice3k_mPing_target

