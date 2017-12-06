png("Zero_mPing.png", width=700, height=400)
library(reshape)
library(ggplot2)
library(Rmisc)

layout(matrix(c(1,2,3,4),1,4), c(0.4,0.4,0.4,0.4))

zero_mping = read.table("Zero_mPing_strains.list")
ping <- read.table("ping_3k.txt")
rownames(ping) <- ping[,1]
ping <- ping[,-2]
ping <- ping[,-1]
ping <- ping[zero_mping[,1],]
ping <- ping[,1001:6339]
#mping
mping <- cbind(ping[,1:253], ping[,5163:5339])
mping <- t(mping)
mping_matrix <- as.matrix(mping)
image(1:430, 1:220, mping_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("mPing", side=1, line=3, font=3, cex=1.2)
mtext("O. sativa", side=2, line=3, font=3, cex=1.2)
axis(2, at=c(1, 100, 200, 220), labels=c(1, 100, 200, 220), cex.lab=1.2)


#ping
ping <- t(ping)
ping_matrix <- as.matrix(ping)
image(1:5339, 1:220, ping_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Ping", side=1, line=3, font=3, cex=1.2)
#mtext("O. sativa", side=2, line=3, font=3, cex=1.2)
#axis(2, at=c(1, 100, 200, 220), labels=c(1, 100, 200, 220), cex.lab=1.2)

pong <- read.table("pong_3k.txt")
rownames(pong) <- pong[,1]
pong <- pong[,-2]
pong <- pong[,-1]
pong <- pong[zero_mping[,1],]
pong <- pong[,1001:6164]
pong <- t(pong)
pong_matrix <- as.matrix(pong)
image(1:5164, 1:220, pong_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Pong", side=1, line=3, font=3, cex=1.2)

actin <- read.table("actin_3k.txt")
rownames(actin) <- actin[,1]
actin <- actin[,-2]
actin <- actin[,-1]
actin <- actin[zero_mping[,1],]
control <- t(actin)
control_matrix <- as.matrix(control)
image(1:5874, 1:220, control_matrix, axes=FALSE, xlab = "", ylab = "", col = c("palegoldenrod", "cadetblue3"))
mtext("Actin", side=1, line=3, font=1, cex=1.2)

dev.off()
