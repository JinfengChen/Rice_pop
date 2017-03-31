pdf("zoomin.pdf", width=12, height=7)
layout(matrix(c(1,2,3), 1, 3, byrow = TRUE), widths=c(1,1,1))
library("plotrix")
par(mar=c(7,5,4,2))
#mPing
mping_data <- read.table("Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.merge.frequency", sep="\t", header=F)
mping <- mping_data[,6]
breaks <- seq(1, 1800, by=1)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, include.lowest=TRUE, right=FALSE, xaxt='n', col="cornflowerblue", ylab="Number of unique Pong loci in 3,000 rice (n=2013)", xlab="Number of strains sharing mPing loci in 3,000 rice", main="", cex=1.4, cex.lab=1.4,cex.axis=1.4, cex.sub=1.4, plot=FALSE)

hist_data

#cut y[1] value
#max is 1215
cut <- 960 # 1215-255, ture value - target value
y <- hist_data$counts[1:100]
y[1]<- y[1] - cut
xx <- barplot(y, ylab="", col="cornflowerblue", axes=FALSE, border=FALSE, ylim=c(0, 300))

#add axis
#y
axis(2, seq(0, 300, by=50), line=0, labels=c(0, 50, 100, 150, 200, 1200, 1300), cex=1.4, cex.axis=1.4, cex.lab=1.4)
mtext('Number of unique mPing loci in 3,000 rice (n=1969)', side=2, line=3, cex=1.4)
#x
#axis(1, xx, line=0,labels=xx,cex=1.4)
interval=24
axis(1, c(0, interval*1, interval*2, interval*3, interval*4, 120), line=1, labels=c("", "","","","",""), cex=1.4, cex.axis=1.4, cex.lab=1.4)
text(c(0, interval*1, interval*2, interval*3, interval*4, 120), rep(-20, 4), labels=c(0, 20, 40, 60, 80, 100), xpd=TRUE, cex=1.4)
mtext('Number of strains sharing mPing loci', side=1, line=5, cex=1.4)

#break y
b <- 220
axis.break(2, b, style="slash")
rect(-0.2, b, max(xx)+0.8, b+2,border=FALSE,col='white')

#Pong
pong_data <- read.table("Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.merge.frequency", sep="\t", header=F)
pong <- pong_data[,6]
breaks <- seq(1, 1200, by=1)
hist_data <- hist(pong, breaks=breaks, freq=TRUE, include.lowest=TRUE, right=FALSE, xaxt='n', col="cornflowerblue", ylab="Number of unique Pong loci in 3,000 rice (n=454)", xlab="Number of strains sharing Pong loci in 3,000 rice", main="", cex=1.4, cex.lab=1.4,cex.axis=1.4, cex.sub=1.4, plot=FALSE)

hist_data

#cut y[1] value
#cut <- 299
#y   <- hist_data$counts
#y[1]<- y[1] - cut
y <- hist_data$counts[1:100]
xx <- barplot(y, ylab="", col="cornflowerblue", axes=FALSE, border=FALSE, ylim=c(0, 250))

#add axis
#y
axis(2, seq(0, 250, by=50), line=0, labels=c(0, 50, 100, 150, 200, 250), cex=1.4, cex.axis=1.4, cex.lab=1.4)
mtext('Number of unique Pong loci in 3,000 rice (n=424)', side=2, line=3, cex=1.4)
#x
#axis(1, xx, line=0,labels=xx,cex=1.4)
i=24
axis(1, c(0, 1*i, 2*i, 3*i, 4*i, 5*i), line=1, labels=c("","","","","",""), cex=1.4, cex.axis=1.4, cex.lab=1.4)
text(c(0, 1*i, 2*i, 3*i, 4*i, 5*i), rep(-20, 7), labels=c(0, 20, 40, 60, 80, 100), xpd=TRUE, cex=1.4)
mtext('Number of strains sharing Pong loci', side=1, line=5, cex=1.4)

#break y
#b <- 45
#axis.break(2, b, style="slash")
#rect(-0.2, b, max(xx)+0.8, b+2,border=FALSE,col='white')

dev.off()
