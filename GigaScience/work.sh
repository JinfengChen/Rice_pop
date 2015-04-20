echo "prepare download link in table"
python merge_inf.py
cat rice_line_IRRI_2466_* > rice_line_IRRI_2466.download.list

echo "generate tree view annotaion table"
python merge_anno.py --mode R
cp rice_line_ALL_3000.anno.list rice_line_ALL_3000.anno.R.list
python merge_anno.py --mode figtree
cp rice_line_ALL_3000.anno.list rice_line_ALL_3000.anno.figtree.list
python merge_anno.py
cat rice_line_ALL_3000.anno.landrice.list >> rice_line_ALL_3000.anno.list

