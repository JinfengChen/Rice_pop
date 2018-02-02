pdf("single_run_colored_defined.pdf", width=7, height=9)
layout(matrix(c(1,2,3,4),1,4),c(0.4, 0.3, 0.2, 0.2))
#par(mar=c(4,1,2,4))
#order: bottom, left, top, and right. The default is c(5.1, 4.1, 4.1, 2.1).
par(mar=c(4,5,2,4))

i = 8
filename <- paste("core_v0.7.pruneddata3.", i, ".Q.reordered.txt", sep="")
tbl <- read.table(filename, sep="\t")
colname  <- paste("core_v0.7.pruneddata3.", i, ".Q.color.txt", sep="")
color <- read.table(colname, sep="\t")
barplot(t(as.matrix(tbl)), space = c(0.2), col=as.vector(color$V3), xlab="", ylab="", border=NA, horiz=TRUE, axes=FALSE)
text(0.25, 3700, labels = paste("K = ", i, sep=""), cex = 1.4, col="black", srt = 1, adj = 0, xpd = TRUE)

par(las=2)
mtext("TRJ", side = 2, font=1, at = 200, line= 3, cex=1, adj = 0, col="cornflowerblue")
mtext("TEJ", side = 2, font=1, at = 800, line= 3, cex=1, adj = 0, col="blue")
mtext("ARO", side = 2, font=1, at = 1150, line= 3, cex=1, adj = 0, col="darkorchid")
mtext("AUS", side = 2, font=1, at = 1350, line= 3, cex=1, adj = 0, col="chocolate")
mtext("IND", side = 2, font=1, at = 2500, line= 3, cex=1, adj = 0, col="green")

#tbl <- read.table("core_v0.7.pruneddata3.8.Q.reordered.txt", sep="\t")
#tbl <- tbl[order(tbl$V1,tbl$V2,tbl$V3,tbl$V4,tbl$V5,tbl$V6,tbl$V7,tbl$V8),]
#color <- c("green", 'blue', 'cornflowerblue', 'green', 'green', 'darkorchid', 'chocolate', 'green')
#color <- read.table('core_v0.7.pruneddata3.8.Q.color.txt', sep="\t")
#barplot(t(as.matrix(tbl)), space = c(0.2), col=as.vector(color$V3), xlab="", ylab="", border=NA, horiz=TRUE)

#tbl <- read.table("core_v0.7.pruneddata3.9.Q.reordered.txt")
#color <- read.table('core_v0.7.pruneddata3.9.Q.color.txt', sep="\t")
#barplot(t(as.matrix(tbl)), space = c(0.2), col=as.vector(color$V3), xlab="", ylab="", border=NA, horiz=TRUE)

dev.off()

