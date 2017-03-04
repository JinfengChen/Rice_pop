python OtherTE_LTR_Table.py --input OtherTE_LTR_RelocaTE2.summary > OtherTE_LTR_RelocaTE2.summary.list
python OtherTE_DNA_Table.py --input OtherTE_DNA_RelocaTE2.summary > OtherTE_DNA_RelocaTE2.summary.list
cat OtherTE_LTR_RelocaTE2.summary.R | R --slave
cat OtherTE_DNA_RelocaTE2.summary.R | R --slave
