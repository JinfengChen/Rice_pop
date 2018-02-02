pdf("multi_run_raw.pdf", width=14, height=18)
layout(matrix(1:14, 14, 1), rep(1, 13))
#order: bottom, left, top, and right. The default is c(5.1, 4.1, 4.1, 2.1).
par(mar=c(1,1,1,7))
for (i in 2:14){
    filename <- paste("core_v0.7.pruneddata3.", i, ".Q.reordered.txt", sep="")
    tbl <- read.table(filename, sep="\t")
    #colname  <- paste("core_v0.7.pruneddata3.", i, ".Q.color.txt", sep="")
    #color <- read.table(colname, sep="\t")
    #barplot(t(as.matrix(tbl)), space = c(0.2), col=as.vector(color$V3), xlab="", ylab="", border=NA, horiz=FALSE, axes=FALSE)
    #mtext(paste("K = ", i, sep=""), side = 4, font=1, at = 0.4, line=1, cex=1.4, col="black")
    #barplot(t(as.matrix(tbl)), space = c(0.2), col=rainbow(14), xlab="", ylab="", border=NA, horiz=FALSE, axes=FALSE)
    text(3700, 0.5, labels = paste("K = ", i, sep=""), cex=3, col="black", srt = 0, adj = 0, xpd = TRUE)
}
