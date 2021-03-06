
library("ape")
tree = read.tree(file="RAxML_bipartitions.Wildrice_Outgroup_rufi48_Hom_norepeat_SNP_qsub.raxml_BS.clean.tree")
tree$edge.length[tree$edge.length<0]<-0
x = read.table(file="Rufipogon_57_RelocaTE2.mPing_Ping_Pong.copy.depth.group.txt", sep='\t', header=1)
y1 = setNames(x[,2], x[,1])
y1 = y1[match(gsub("'", '', tree$tip.label), names(y1))]
y2 = setNames(x[,3], x[,1])
y2 = y2[match(gsub("'", '', tree$tip.label), names(y2))]
y3 = setNames(x[,4], x[,1])
y3 = y3[match(gsub("'", '', tree$tip.label), names(y3))]

sample_colors = setNames(x[,7], x[,1])
sample_colors = sample_colors[match(gsub("'", '', tree$tip.label), names(sample_colors))]
sample_colors = as.vector(sample_colors)

pdf("Rufipogon_57_RelocaTE2.mPing_Ping_Pong.pdf", width=7, height=9)
layout(matrix(c(1,2,3,4),1,4),c(0.6, 0.2, 0.2, 0.2))
par(mar=c(4,1,2,1))
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

plot(tree, edge.color=edge_colors, use.edge.length=FALSE, tip.color=sample_colors,  show.tip.label = TRUE, cex = 1, underscore=TRUE)
leg_inf = cbind(as.vector(x[,2]), as.vector(x[,6]))
leg_inf = unique(leg_inf)
leg_inf = leg_inf[order(leg_inf[,2]),]
xrange  = par("xaxp")
yrange  = par("yaxp")
par(xpd=TRUE) #set this legend can be plot into margin area
#legend(x=xrange[2]*0.8, y=yrange[2]*0.99, substr(leg_inf[,2], 1, 4), fill=leg_inf[,1], border=FALSE, bty='n')
#legend(x=xrange[2]*0.6, y=yrange[2]*0.99, leg_inf[,2], fill=leg_inf[,1], border=FALSE, bty='n', cex=1.4)
par(font=3)
legend(x=xrange[2]*0.1, y=yrange[2]*0.1, c("Or-I", "Or-II", "Or-IIIa", "Or-IIIb", "Outgroup"), fill=c("brown", "blue", "orange", "red", "black"), border=FALSE, bty='n', cex=1.4)
par(font=1)
#par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at= c(0, 100, 200), line=1)
#mping
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y1,horiz=TRUE,width=1,space=0, xlim=c(0, 20),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 10, 20), line=0)
mtext("mPing", side=1,font=3, at=10,line=2.5, cex=1, col="black")
#ping
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y2,horiz=TRUE,width=1,space=0, xlim=c(0, 4),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 2, 4), line=0)
mtext("Ping", side=1,font=3, at=2,line=2.5, cex=1, col="black")
#pong
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y3,horiz=TRUE,width=1,space=0, xlim=c(0, 10),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 5, 10), line=0)
mtext("Pong", side=1,font=3, at=5,line=2.5, cex=1, col="black")
dev.off()

