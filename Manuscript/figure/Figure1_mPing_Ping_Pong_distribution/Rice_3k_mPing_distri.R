pdf("Rice_3k_mPing_distri.pdf")
par(mar=c(5,5,4,2))
mping_data <- read.table("Transposon_mPing_Ping_Pong.3k_mPing.summary", sep="\t", header=T)
mping <- mping_data[,2]
breaks <- seq(0,200, by=5)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, col="cornflowerblue", ylab="Number of strains (n=3000)", xlab="mPing copy mumber", main="", cex=1.4, cex.lab=1.4,cex.axis=1.4, cex.sub=1.4)
dev.off()
