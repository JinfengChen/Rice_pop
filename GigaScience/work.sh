echo "prepare download link in table"
python merge_inf.py
cat rice_line_IRRI_2466_* > rice_line_IRRI_2466.download.list

echo "generate tree view annotaion table"
python merge_anno.py

