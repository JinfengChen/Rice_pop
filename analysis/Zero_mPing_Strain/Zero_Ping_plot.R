pdf("Zero_Ping.pdf", width=7, height=4)
par(mar=c(5,5,4,2))
library(reshape)
library(ggplot2)
library(Rmisc)

layout(matrix(c(1,2,3,4),1,4), c(0.3,0.25,0.25,0.25))

zero_mping = read.table("Zero_Ping_strains.list")
ping <- read.table("ping_3k_NM2.txt")
rownames(ping) <- ping[,1]
ping <- ping[,-2]
ping <- ping[,-1]
#ping <- ping[zero_mping[,1],]
ping <- subset(ping, row.names(ping) %in% zero_mping[,1])
#ping <- ping[,1001:6339]
#mping
#mping <- cbind(ping[,1:253], ping[,5163:5339])
#mping <- t(mping)
#mping_matrix <- as.matrix(mping)
#image(1:430, 1:2749, mping_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
#mtext("mPing", side=1, line=3, font=3, cex=1.2)
#mtext("O. sativa", side=2, line=3, font=3, cex=1.2)
#axis(2, at=c(1, 500, 1000, 1500, 2000, 2500, 2749), labels=c(1, 500, 1000, 1500, 2000, 2500, 2749), cex.lab=1.2)

#mping
mping <- read.table("mping_3k_NM2.txt")
rownames(mping) <- mping[,1]
mping <- mping[,-2]
mping <- mping[,-1]
#mping <- mping[zero_mping[,1],]
mping <- subset(mping, row.names(mping) %in% zero_mping[,1])
mping <- t(mping)
mping_matrix <- as.matrix(mping)
image(1:429, 1:2749, mping_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("mPing", side=1, line=3, font=3, cex=1.2)
mtext("Rice strains", side=2, line=3, font=1, cex=1.2)
axis(2, at=c(1, 2749), labels=c(1, 2749), cex.lab=1.4, cex.axis=1.4)
axis(1, at=c(0.5, 429), labels=c(1, 430), cex.lab=1.4, cex.axis=1.4)

par(mar=c(5,2,4,2))
#ping
ping <- t(ping)
ping_matrix <- as.matrix(ping)
image(1:5340, 1:2749, ping_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Ping", side=1, line=3, font=3, cex=1.2)
axis(1, at=c(0.5, 5340), labels=c(1, 5341), cex.lab=1.4, cex.axis=1.4)
#mtext("O. sativa", side=2, line=3, font=3, cex=1.2)
#axis(2, at=c(1, 100, 200, 220), labels=c(1, 100, 200, 220), cex.lab=1.2)

par(mar=c(5,2,4,2))
#pong
pong <- read.table("pong_3k_NM2.txt")
rownames(pong) <- pong[,1]
pong <- pong[,-2]
pong <- pong[,-1]
#pong <- pong[zero_mping[,1],]
pong <- subset(pong, row.names(pong) %in% zero_mping[,1])
#pong <- pong[,1001:6164]
pong <- t(pong)
pong_matrix <- as.matrix(pong)
image(1:5165, 1:2749, pong_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Pong", side=1, line=3, font=3, cex=1.2)
axis(1, at=c(0.5, 5165), labels=c(1, 5166), cex.lab=1.4, cex.axis=1.4)

par(mar=c(5,2,4,2))
actin <- read.table("actin_3k_NM2.txt")
rownames(actin) <- actin[,1]
actin <- actin[,-2]
actin <- actin[,-1]
#actin <- actin[zero_mping[,1],]
actin <- subset(actin, row.names(actin) %in% zero_mping[,1])
control <- t(actin)
control_matrix <- as.matrix(control)
image(1:5875, 1:2749, control_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Actin", side=1, line=3, font=1, cex=1.2)
axis(1, at=c(0.5, 5875), labels=c(1, 5876), cex.lab=1.4, cex.axis=1.4)

dev.off()
