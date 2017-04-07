pdf("mPing_Ping_Pong_pie.pdf")
library(plyr)
par(mar=c(4,4,4,2))
mpingdata <- read.table("rice_line_ALL_3000.anno.landrace.list.txt", sep="\t", header=TRUE)
grouplist <- mpingdata[mpingdata$mPing==0, ]$Group
grouplist <- gsub("jap", "japonica", grouplist)
p <- count(grouplist)
color <- c("chocolate", "darkorchid", "green", "black", "cyan", "blue", "cornflowerblue")
pie(p$freq, labels=p$x, font=3, col=color)
dev.off()

