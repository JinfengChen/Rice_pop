library("plotrix")
library("ape")
tree = read.tree(file="3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.landrace_group.tree")
tree$edge.length[tree$edge.length<0]<-0
x = read.table(file="3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.landrace_group.anno", sep='\t', header=1)
y1 = setNames(x[,7], x[,1])
y1 = y1[match(gsub("'", '', tree$tip.label), names(y1))]
y2 = setNames(x[,8], x[,1])
y2 = y2[match(gsub("'", '', tree$tip.label), names(y2))]

sample_colors = setNames(x[,2], x[,1])
sample_colors = sample_colors[match(gsub("'", '', tree$tip.label), names(sample_colors))]
sample_colors = as.vector(sample_colors)

pdf("3K_coreSNP-v2.1.binary.tab.landrace.nj.tree.landrace_group.tree_mPing_Ping.pdf", width=10, height=12)
layout(matrix(c(1,2,3),1,3),c(0.5, 0.3, 0.2))
par(mar=c(4,1,0.5,0))
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

plot(tree, edge.color=edge_colors, show.tip.label = TRUE, cex = 0.8, underscore=TRUE)
leg_inf = cbind(as.vector(x[,2]), as.vector(x[,6]))
leg_inf = unique(leg_inf)
leg_inf = leg_inf[order(leg_inf[,2]),]
xrange  = par("xaxp")
yrange  = par("yaxp")
par(xpd=TRUE) #set this legend can be plot into margin area
#legend(x=xrange[2]*0.8, y=yrange[2]*0.99, substr(leg_inf[,2], 1, 4), fill=leg_inf[,1], border=FALSE, bty='n')
legend(x=xrange[2]*0.7, y=yrange[2]*0.99, leg_inf[,2], fill=leg_inf[,1], border=FALSE, bty='n', cex=1.4)

#par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at= c(0, 100, 200), line=1)
#mping

par(mar=c(4,0.5, 0, 3)) #set left and right to be tight with other plot
cut <- 140
#new scale 300 to 600 cresponding to 160 and 200. So the factor is 300/40=7.5
#new value should be (503-140)/7.5 + 120
for(i in 1:length(y1)){
   #print(y1[i])
   if (!is.na(y1[i])){
       if (y1[i] > 120){
           y1[i] <- (y1[i] - cut)/7.5 + 140
       }
   }
} 

#barplot(y1,horiz=TRUE,width=1,space=0, xlim=c(0, 600),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
xx <- barplot(y1,horiz=TRUE,width=1,space=0, xlim=c(0, 180),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at=c(0, 40, 80, 120, 160, 200), labels=c(0, 40, 80, 120, 300, 600), line=0)
mtext("mPing", side=1,font=3, at=90,line=2.5, cex=1, col="black")
#break y
b <- 135
axis.break(1, b, style="slash")
rect(b, 0.2, b+2, max(xx)+0.8, border=FALSE, col='white')


#ping
par(mar=c(4,0.5, 0, 1)) #set left and right to be tight with other plot
barplot(y2,horiz=TRUE,width=1,space=0, xlim=c(0, 10),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 5, 10), line=0)
mtext("Ping", side=1,font=3, at=5,line=2.5, cex=1, col="black") 
dev.off()

