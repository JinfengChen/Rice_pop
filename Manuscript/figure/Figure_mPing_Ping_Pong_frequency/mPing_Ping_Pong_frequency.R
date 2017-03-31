pdf("mPing_Ping_Pong_frequency.pdf", width=12, height=7)
layout(matrix(c(1,2,3), 1, 3, byrow = TRUE), widths=c(1,1,1))
library("plotrix")
par(mar=c(7,5,4,2))
#mPing
mping_data <- read.table("Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.merge.frequency", sep="\t", header=F)
mping <- mping_data[,6]
breaks <- seq(0, 1800, by=100)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, include.lowest=TRUE, right=FALSE, xaxt='n', col="cornflowerblue", ylab="Number of unique Pong loci in 3,000 rice (n=2013)", xlab="Number of strains sharing mPing loci in 3,000 rice", main="", cex=1.4, cex.lab=1.4,cex.axis=1.4, cex.sub=1.4, plot=FALSE)

hist_data

#cut y[1] value
cut <- 1898
y   <- hist_data$counts
y[1]<- y[1] - cut
xx <- barplot(y, ylab="", col="cornflowerblue", axes=FALSE, border=TRUE, ylim=c(0, 80))

#add axis
#y
axis(2, seq(0, 80, by=20), line=0, labels=c(0, 20, 40, 1800, 2000), cex.axis=1.2)
mtext('Number of unique mPing loci in 3,000 rice (n=2013)', side=2, line=3, cex=1.2)
#x
#axis(1, xx, line=0,labels=xx,cex=1.4)
axis(1, c(0, 5.5+0.6, 11.5+0.6, 17.5+0.6, 22), line=1, labels=c("","","","",""), cex=1.2)
text(c(0, 5.5+0.6, 11.5+0.6, 17.5+0.6, 22), rep(-5, 4), labels=c(0, 500, 1000, 1500, 1800), xpd=TRUE, cex=1.2)
mtext('Number of strains sharing mPing loci', side=1, line=5, cex=1.2)

#break y
b <- 50
axis.break(2, b, style="slash")
rect(-0.2, b, max(xx)+0.8, b+2,border=FALSE,col='white')

mtext("A", side=3, line = 1.5, at = -4, cex=1.4)

#Ping
ping_data <- read.table("Rice3k_3000_RelocaTEi_Ping.CombinedGFF.ALL.merge.frequency", sep="\t", header=F)
ping <- ping_data[,6]
breaks <- seq(0, 60, by=1)
hist_data <- hist(ping, breaks=breaks, freq=TRUE, col="cornflowerblue", ylab="Number of unique Ping loci in 3,000 rice (n=43)", xlab="Number of strains sharing Ping loci in 3,000 rice", main="", plot=FALSE)

hist_data

#barplot
y <- hist_data$counts
barplot(y, ylab="", col="cornflowerblue", axes=FALSE, border=TRUE, ylim=c(0, 20))

#add axis
#y
axis(2, seq(0, 20, by=5), line=0, labels=c(0, 5, 10, 15, 20), cex.axis=1.2)
mtext('Number of unique Ping loci in 3,000 rice (n=43)', side=2, line=3, cex=1.2)
#x
i=12
axis(1, c(0, 1*i, 2*i, 3*i, 4*i, 5*i, 6*i), line=1, labels=c("","","","","","",""), cex=1.2)
text(c(0, 1*i, 2*i, 3*i, 4*i, 5*i, 6*i), rep(-1.3, 7), labels=c(0, 10, 20, 30, 40, 50, 60), xpd=TRUE, cex=1.2)
mtext('Number of strains sharing Ping loci', side=1, line=5, cex=1.2)

mtext("B", side=3, line = 1.5, at = -14, cex=1.4)

#Pong
pong_data <- read.table("Rice3k_3000_RelocaTEi_Pong.CombinedGFF.ALL.merge.frequency", sep="\t", header=F)
pong <- pong_data[,6]
breaks <- seq(0, 1200, by=10)
hist_data <- hist(pong, breaks=breaks, freq=TRUE, include.lowest=TRUE, right=FALSE, xaxt='n', col="cornflowerblue", ylab="Number of unique Pong loci in 3,000 rice (n=454)", xlab="Number of strains sharing Pong loci in 3,000 rice", main="", cex=1.4, cex.lab=1.4,cex.axis=1.4, cex.sub=1.4, plot=FALSE)

hist_data

#cut y[1] value
cut <- 299
y   <- hist_data$counts
y[1]<- y[1] - cut
xx <- barplot(y, ylab="", col="cornflowerblue", axes=FALSE, border=TRUE, ylim=c(0, 60))

#add axis
#y
axis(2, seq(0, 60, by=10), line=0, labels=c(0, 10, 20, 30, 40, 300, 400), cex.axis=1.2)
mtext('Number of unique Pong loci in 3,000 rice (n=454)', side=2, line=3, cex=1.2)
#x
#axis(1, xx, line=0,labels=xx,cex=1.4)
i=24
axis(1, c(0, 1*i, 2*i, 3*i, 4*i, 5*i, 6*i), line=1, labels=c("","","","","","",""), cex=1.2)
text(c(0, 1*i, 2*i, 3*i, 4*i, 5*i, 6*i), rep(-4.5, 7), labels=c(0, 200, 400, 600, 800, 1000, 1200), xpd=TRUE, cex=1.2)
mtext('Number of strains sharing Pong loci', side=1, line=5, cex=1.2)

#break y
b <- 45
axis.break(2, b, style="slash")
rect(-0.2, b, max(xx)+0.8, b+2,border=FALSE,col='white')

mtext("C", side=3, line = 1.5, at = -32, cex=1.4)

dev.off()

