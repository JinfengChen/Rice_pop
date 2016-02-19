library(ape)
#phy<-rtree(12)
#l<-subtrees(phy)
tree = read.tree(file="3K_coreSNP-v2.1.binary.tab.landrace.nj.tree")
l <- subtrees(tree)
for (i in 1:length(l)){
    #print(i)
    #print(length(l[[i]]$tip.label))
    if (length(l[[i]]$tip.label) == 136){
        #print(length(l[[i]]$tip.label))
        #print(l[[i]]$tip.label)
        write.table(l[[i]]$tip.label, file="subtree.tip", sep=",", quote=FALSE, row.names=FALSE, col.names=FALSE, append=TRUE)
        #plot(l[[i]])
    } 
}
