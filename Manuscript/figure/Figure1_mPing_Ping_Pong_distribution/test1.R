pdf("test1.pdf", width=6, height=7)
par(mar=c(5,5,4,2))
mping_data <- read.table("Transposon_mPing_Ping_Pong.3k_mPing.summary", sep="\t", header=T)
mping <- mping_data[,2]
breaks <- seq(0,200, by=5)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, col="cornflowerblue", ylab="Number of strains (n=3000)", xlab="mPing copy mumber", main="", cex=1.8, cex.lab=1.8,cex.axis=1.8)
#hist_data$counts[1] <- hist_data$counts[1] - 250
#hist_data$counts[2] <- hist_data$counts[2] - 250
#hist_data$counts[3] <- hist_data$counts[3] - 250
#hist_data$counts[4] <- hist_data$counts[4] - 250
plot(hist_data, ylim=c(0, 60), col="cornflowerblue", ylab="Number of strains (n=3000)", xlab="mPing copy mumber", main="", cex=2, cex.lab=2,cex.axis=2)
dev.off()
