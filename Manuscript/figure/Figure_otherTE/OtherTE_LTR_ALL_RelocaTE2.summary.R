library("plotrix")
library("ape")
tree = read.tree(file="3K_coreSNP-v2.1.binary.tab.landrace.nj.tree")
tree$edge.length[tree$edge.length<0]<-0
x = read.table(file="OtherTE_LTR_ALL_RelocaTE2.summary.list", sep='\t', header=1)
y1 = setNames(x[,7], x[,1])
y1 = y1[match(gsub("'", '', tree$tip.label), names(y1))]
y2 = setNames(x[,8], x[,1])
y2 = y2[match(gsub("'", '', tree$tip.label), names(y2))]
y3 = setNames(x[,9], x[,1])
y3 = y3[match(gsub("'", '', tree$tip.label), names(y3))]
y4 = setNames(x[,10], x[,1])
y4 = y4[match(gsub("'", '', tree$tip.label), names(y4))]
y5 = setNames(x[,11], x[,1])
y5 = y5[match(gsub("'", '', tree$tip.label), names(y5))]
y6 = setNames(x[,12], x[,1])
y6 = y6[match(gsub("'", '', tree$tip.label), names(y6))] 
y7 = setNames(x[,13], x[,1])
y7 = y7[match(gsub("'", '', tree$tip.label), names(y7))] 


sample_colors = setNames(x[,2], x[,1])
sample_colors = sample_colors[match(gsub("'", '', tree$tip.label), names(sample_colors))]
sample_colors = as.vector(sample_colors)

pdf("OtherTE_LTR_ALL_RelocaTE2.summary.pdf", width=10, height=9)
layout(matrix(c(1,2,3,4,5,6,7,8),1,8),c(0.3, 0.1, 0.1, 0.1,0.1, 0.1, 0.1, 0.1))
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

plot(tree, edge.color=edge_colors, show.tip.label = FALSE, cex = 0.5, underscore=TRUE)
leg_inf = cbind(as.vector(x[,2]), as.vector(x[,6]))
leg_inf = unique(leg_inf)
leg_inf = leg_inf[order(leg_inf[,2]),]
xrange  = par("xaxp")
yrange  = par("yaxp")
par(xpd=TRUE) #set this legend can be plot into margin area
#legend(x=xrange[2]*0.8, y=yrange[2]*0.99, substr(leg_inf[,2], 1, 4), fill=leg_inf[,1], border=FALSE, bty='n')
legend(x=xrange[2]*0.6, y=yrange[2]*0.99, leg_inf[,2], fill=leg_inf[,1], border=FALSE, bty='n', cex=1.4)

#par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#barplot(y,horiz=TRUE,width=1,space=0, xlim=c(-10, 200),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at= c(0, 100, 200), line=1)
#mping
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#cut <- 100
#new scale 300 to 600 cresponding to 120 and 150. So the factor is 300/30=10
#new value should be (503-140)/7.5 + 120
#for(i in 1:length(y1)){
#   if (y1[i] > 110){
#       y1[i] <- (y1[i] - cut)/10 + 100
#   }
#} 

#xx <- barplot(y1,horiz=TRUE,width=1,space=0, xlim=c(0, 150),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at=c(0, 30, 60, 90, 120, 150), labels=c(0, 30, 60, 90, 300, 600), line=0)
#mtext("mPing", side=1,font=3, at=70,line=2.5, cex=1, col="black")
#break y
#break y
#b <- 100
#axis.break(1, b, style="slash")
#rect(b, 0.2, b+2, max(xx)+0.8, border=FALSE, col='white')

#Bajie	Dasheng	Retro1	RIRE2	RIRE3	Copia2
#1
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y1,horiz=TRUE,width=1,space=0, xlim=c(0, 3),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 1, 2, 3), line=0)
mtext("Bajie", side=1,font=3, at=1.5,line=2.5, cex=1, col="black")
#2
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y2,horiz=TRUE,width=1,space=0, xlim=c(0, 60),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 20, 40, 60), line=0)
mtext("Dasheng", side=1,font=3, at=30,line=2.5, cex=1, col="black")
#3
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y3,horiz=TRUE,width=1,space=0, xlim=c(0, 30),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 10, 20, 30), line=0)
mtext("Retro1", side=1,font=3, at=15,line=2.5, cex=1, col="black")
#4
#par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#barplot(y4,horiz=TRUE,width=1,space=0, xlim=c(0, 180),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at= c(0, 60, 120, 180), line=0)
#mtext("RIRE2", side=1,font=3, at=100,line=2.5, cex=1, col="black")
#5
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y5,horiz=TRUE,width=1,space=0, xlim=c(0, 300),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 100, 200, 300), line=0)
mtext("RIRE3", side=1,font=3, at=150,line=2.5, cex=1, col="black")
#6
par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
barplot(y6,horiz=TRUE,width=1,space=0, xlim=c(0, 15),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
axis(1, at= c(0, 5, 10, 15), line=0)
mtext("Copia2", side=1,font=3, at=8,line=2.5, cex=1, col="black")
#7
#par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#barplot(y7,horiz=TRUE,width=1,space=0, xlim=c(0, 3),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at= c(0, 1, 2, 3), line=0)
#mtext("Pong", side=1,font=3, at=10,line=2.5, cex=1, col="black")


#ping
#par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#barplot(y2,horiz=TRUE,width=1,space=0, xlim=c(0, 10),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at= c(0, 5, 10), line=0)
#mtext("Ping", side=1,font=3, at=5,line=2.5, cex=1, col="black")
#pong
#par(mar=c(4,0.5, 2, 1)) #set left and right to be tight with other plot
#barplot(y3,horiz=TRUE,width=1,space=0, xlim=c(0, 20),  ylim=c(0.5,length(tree$tip.label)),names="", axes=FALSE)
#axis(1, at= c(0, 10, 20), line=0)
#mtext("Pong", side=1,font=3, at=10,line=2.5, cex=1, col="black")
dev.off()

