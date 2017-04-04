#high frequency pong not assoicated with selection sweep
bedtools window -a ALL.sweep.unique.bed -b Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.merge.frequency | awk '$9>100'

