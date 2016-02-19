
library("ape")
tree = read.tree(file="3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree.indica.tree")
x = read.table(file="3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree.indica.anno", sep='\t', header=1)
y = setNames(x[,7], x[,1])
y = y[match(gsub("'", '', tree$tip.label), names(y))]

sample_colors = setNames(x[,2], x[,1])
sample_colors = sample_colors[match(gsub("'", '', tree$tip.label), names(sample_colors))]
sample_colors = as.vector(sample_colors)

pdf("3K_coreSNP-v2.1.pruneddata.tab.fasttree.nj.tree.indica.pdf")
layout(matrix(c(1,2),1,2),c(0.7,0.3))
par(mar=c(4,1,2,2))
edge_colors=NULL

#https://ecomorph.wordpress.com/2014/10/09/phylogenetic-trees-in-r-4/
#edge_num includes all the edge of internal edge or termial edge.
#the latter is what we need.
edge_num = tree$edge[,2]
for (i in 1:length(edge_num)){
     if (edge_num[i] > length(sample_colors)){
         edge_colors[i] = 'black'
     }else{
         edge_colors[i] = sample_colors[edge_num[i]]
     }
}

plot(tree, edge.color=edge_colors, show.tip.label = FALSE)

barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 100, 200), line=1)
dev.off()

