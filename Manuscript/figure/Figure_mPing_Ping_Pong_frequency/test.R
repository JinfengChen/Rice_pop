pdf("mPing_Ping_Pong_frequency.pdf", width=12, height=7)
layout(matrix(c(1,2,3), 1, 3, byrow = TRUE), widths=c(1,1,1))
library("plotrix")
par(mar=c(7,5,4,2))
#mPing
mping_data <- read.table("Rice3k_3000_RelocaTEi_mPing.CombinedGFF.ALL.merge.frequency", sep="\t", header=F)
mping <- mping_data[,6]
breaks <- seq(0, 1800, by=100)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, include.lowest=TRUE, right=FALSE, xaxt='n', col="cornflowerblue", ylab="Number of unique Pong loci in 3,000 rice (n=2013)", xlab="Number of strains sharing mPing loci in 3,000 rice", main="", cex=1.4, cex.lab=1.4,cex.axis=1.4, cex.sub=1.4, plot=FALSE)
cut <- 1898
y   <- hist_data$counts
y[1]<- y[1] - cut
xx <- barplot(y, ylab="", col="cornflowerblue", border=TRUE, ylim=c(0, 80))
library("Hmisc")
subplot(barplot(hist_data$count[1:100], ylab="", col="cornflowerblue", axes=FALSE, border=TRUE), 15, 50, size=c(3,2))
dev.off()

