png("Zero.png", width=700, height=400)
library(reshape)
library(ggplot2)
library(Rmisc)

layout(matrix(c(1,2,3),1,3), c(0.47,0.4,0.4))

#ping
par(mar=c(5,5,4,1))
ping <- read.table("ping_3k.txt")
ping <- ping[,1001:6339]
ping <- t(ping)
ping_matrix <- as.matrix(ping)
image(1:5339, 1:3000, ping_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Ping", side=1, line=3, font=3, cex=1.2)
mtext("O. rufipogon", side=2, line=3, font=3, cex=1.2)
axis(2, at=c(1, 500, 1000, 1500, 2000, 2500, 3000), labels=c(1, 500, 1000, 1500, 2000, 2500, 3000), cex.lab=1.2)
#pong
par(mar=c(5,1,4,1))
pong <- read.table("pong_3k.txt")
pong <- pong[,1001:6164]
pong <- t(pong)
pong_matrix <- as.matrix(pong)
image(1:5164, 1:3000, pong_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Pong", side=1, line=3, font=3, cex=1.2)
#actin
par(mar=c(5,1,4,1))
control <- read.table("actin_3k.txt")
control <- t(control)
control_matrix <- as.matrix(control)
image(1:5874, 1:3000, control_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Control", side=1, line=3, font=1, cex=1.2)
#depth
#par(mar=c(3.7, 1, 2.7, 2))
#depth <- read.table("rice_3k_depth.txt.ordered.header.txt")
#barplot(depth[,2], horiz=TRUE, width=1, space=0, axes=FALSE, xlim=c(0, 60))
#axis(1, at=c(0, 30, 60), line=0, labels=c("0", "30", "60"), cex.lab=1.2)
#mtext("Depth", at=30, side=1, line=2.5, font=1, cex=1.2)

dev.off()

