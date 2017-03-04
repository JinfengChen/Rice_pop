pdf("rice_3k_insertion_size.pdf")
par(mar=c(5,5,4,2))
mping_data <- read.table("rice_3k_insertion_size.txt", sep="\t", header=T)
mping <- mping_data[,2]
breaks <- seq(400, 700, by=10)
hist_data <- hist(mping, breaks=breaks, freq=TRUE, col="cornflowerblue", ylab="Number of strains (n=3000)", xlab="Average library insertion size", main="", cex=1.4, cex.lab=1.4,cex.axis=1.4, cex.sub=1.4)
dev.off()
