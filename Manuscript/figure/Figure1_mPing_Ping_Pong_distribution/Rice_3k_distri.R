pdf("Rice_3k_distri.pdf", width=12, height=7)
layout(matrix(c(1,2,3), 1, 3, byrow = TRUE), widths=c(2,1,2))
#mPing
par(mar=c(5,5,4,2))
mping_data <- read.table("Transposon_mPing_Ping_Pong.3k_mPing.summary", sep="\t", header=T)
mping <- mping_data[,2]
breaks <- seq(0,200, by=5)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, col="cornflowerblue", ylab="Number of strains (n=3000)", xlab="mPing copy mumber", main="", cex=1.8, cex.lab=1.8,cex.axis=1.8, cex.sub=1.8)
mtext("A", side=3, line = 1.5, at = -35, cex=1.4)
#Ping
par(mar=c(5,5,4,2))
mping_data <- read.table("Transposon_mPing_Ping_Pong.3k_Ping.summary", sep="\t", header=T)
mping <- mping_data[,2]
breaks <- seq(0,5, by=1)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, include.lowest=TRUE, right=FALSE, xaxt='n', col="cornflowerblue", ylab="Number of strains (n=3000)", xlab="Ping copy number", main="", cex=1.8, cex.lab=1.8,
cex.axis=1.8, cex.sub=1.8)
axis(1,c(0, 5), line=0, labels=c("",""), cex=1.8)
text(seq(0.5, 4.5,by=1), rep(-200,5), labels=c(0, 1, 2, 3, 4), xpd=TRUE, cex=1.8)
mtext("B", side=3, line = 1.5, at = -2, cex=1.4)
#Pong
par(mar=c(5,5,4,2))
mping_data <- read.table("Transposon_mPing_Ping_Pong.3k_Pong.summary", sep="\t", header=T)
mping <- mping_data[,2]
breaks <- seq(0,30, by=1)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, include.lowest=TRUE, right=FALSE, col="cornflowerblue", ylab="Number of strains (n=3000)", xlab="Pong copy number", main="", cex=1.8, cex.lab=1.8,cex.axis=1.8, cex.sub=1.8)
mtext("C", side=3, line = 1.5, at = -6, cex=1.4)
dev.off()
