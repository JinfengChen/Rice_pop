pdf("Rice_3k_Ping_distri.pdf", width=4, height=7)
par(mar=c(5,5,4,2))
mping_data <- read.table("Transposon_mPing_Ping_Pong.3k_Ping.summary", sep="\t", header=T)
mping <- mping_data[,2]
breaks <- seq(0,5, by=1)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, include.lowest=TRUE, right=FALSE, xaxt='n', col="cornflowerblue", ylab="Number of strains (n=3000)", xlab="Ping copy number", main="", cex=1.4, cex.lab=1.4,cex.axis=1.4, cex.sub=1.4)
axis(1,c(0, 5), line=0, labels=c("",""), cex=1.4)
text(seq(0.5, 4.5,by=1), rep(-200,5), labels=c(0, 1, 2, 3, 4), xpd=TRUE, cex=1.4)
dev.off()
