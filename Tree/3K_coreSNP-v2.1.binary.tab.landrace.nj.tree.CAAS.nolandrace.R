
library("ape")
tree = read.tree(file="3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.CAAS.nolandrace.tree")
x = read.table(file="3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.CAAS.nolandrace.anno", sep='\t', header=1)
y = setNames(x[,7], x[,1])
y = y[match(gsub("'", '', tree$tip.label), names(y))]

sample_colors = setNames(x[,2], x[,1])
sample_colors = sample_colors[match(gsub("'", '', tree$tip.label), names(sample_colors))]
sample_colors = as.vector(sample_colors)

pdf("3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.CAAS.nolandrace.pdf")
layout(matrix(c(1,2),1,2),c(0.7,0.3))
par(mar=c(4,1,2,4))
edge_colors=rep("black", length(tree$edge[,2]))

#https://ecomorph.wordpress.com/2014/10/09/phylogenetic-trees-in-r-4/
#edge_num includes all the edge of internal edge or termial edge.
#the latter is what we need.
edge_num = tree$edge[,2]
for (i in 1:length(edge_num)){
     if (edge_num[i] <= length(sample_colors)){
         if (!is.na(sample_colors[edge_num[i]])){
             edge_colors[i] = sample_colors[edge_num[i]]
         }
     }
}

plot(tree, edge.color=edge_colors, show.tip.label = FALSE)
leg_inf = cbind(as.vector(x[,2]), as.vector(x[,6]))
leg_inf = unique(leg_inf)
leg_inf = leg_inf[order(leg_inf[,2]),]
xrange  = par("xaxp")
yrange  = par("yaxp")
par(xpd=TRUE) #set this legend can be plot into margin area
#legend(x=xrange[2]*0.8, y=yrange[2]*0.99, substr(leg_inf[,2], 1, 4), fill=leg_inf[,1], border=FALSE, bty='n')
legend(x=xrange[2]*0.8, y=yrange[2]*0.99, leg_inf[,2], fill=leg_inf[,1], border=FALSE, bty='n')

par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at= c(0, 100, 200), line=1)
barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 600),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 300, 600), line=1)
dev.off()

