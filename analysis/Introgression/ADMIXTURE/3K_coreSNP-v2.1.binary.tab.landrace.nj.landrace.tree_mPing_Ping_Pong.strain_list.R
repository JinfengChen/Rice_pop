library("plotrix")
library("ape")
tree = read.tree(file="3K_coreSNP-v2.1.binary.tab.landrace.nj.tree")
tree$edge.length[tree$edge.length<0]<-0
x = read.table(file="rice_line_ALL_3000.anno.landrace.list", sep='\t', header=1)
#tree$tip.label
write.table(tree$tip.label, file = "3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.tip.label.txt", append = FALSE, quote = FALSE, sep = "\t", row.names = FALSE, col.names = FALSE)

