pvalue <- function(x1, y1, x2, y2, top, p){
  star <- '*'
  if (p > 0.05) {star <- 'n.s.'}
  if (p < 0.001){ star <- '**'}
  if (p < 0.0001){ star <- '***'}
  segments(x1,y1,x1,top)
  segments(x1,top,x2,top)
  segments(x2,top,x2,y2)
  #segments(x1-0.2,y1,x1+0.2,y1)
  #segments(x2-0.2,y2,x2+0.2,y2)
  xt <- min(x1,x2)+abs(x2-x1)/2
  yt <- top*1.03
  p <- bquote(paste("P", " "<=" ", .(p), sep= ""))
  #pp <- expression("P "<= 2.2e-16)
  #pp <- expression(p)
  #p <- paste(pp, p, sep="")
  text(xt,yt,p, cex=1, xpd=TRUE)
} 

pdf("mPing_Ping_Pong_variation.pdf")
library("beeswarm")
library("plotrix")
par(mar=c(6,5,4,2))
mpingdata <- read.table("rice_line_ALL_3000.anno.landrace.list.txt",header=TRUE, sep="\t")
mpingdata$Group <- factor(mpingdata$Group, levels=c("Indica", "Aus/boro", "Basmati/sadri", "Intermediate", "Japonica", "Temperate jap", "Tropical jap"))

#test
mpingdata1 = mpingdata[mpingdata$mPing<100, ]
wilcox.test(mpingdata1[mpingdata1$Group=='Temperate jap', ]$mPing, mpingdata1[mpingdata1$Group=='Tropical jap', ]$mPing)
wilcox.test(mpingdata1[mpingdata1$Group=='Temperate jap', ]$mPing, mpingdata1[mpingdata1$Group=='Intermediate', ]$mPing)
wilcox.test(mpingdata1[mpingdata1$Group=='Temperate jap', ]$mPing, mpingdata1[mpingdata1$Group=='Indica', ]$mPing)
wilcox.test(mpingdata1[mpingdata1$Group=='Temperate jap', ]$mPing, mpingdata1[mpingdata1$Group=='Aus/boro', ]$mPing)
wilcox.test(mpingdata1[mpingdata1$Group=='Temperate jap', ]$mPing, mpingdata1[mpingdata1$Group=='Japonica', ]$mPing)
wilcox.test(mpingdata1[mpingdata1$Group=='Temperate jap', ]$mPing, mpingdata1[mpingdata1$Group=='Basmati/sadri', ]$mPing)

#cut y
cut <- 100
for(i in 1:length(mpingdata$mPing)){
    if (mpingdata$mPing[i] > 110){
       mpingdata$mPing[i] <- (mpingdata$mPing[i] - cut)/10 + 100
    }
}

#plot
beeswarm(mPing ~ Group, data = mpingdata,
          pch = 16, col=c("cornflowerblue"),
          xlab = "", ylab = "",
          method="swarm", corral="wrap", axes=FALSE, ylim=c(0, 150))
bxplot(mPing ~ Group, data = mpingdata, add=TRUE)
axis(2, at=c(0, 30, 60, 90, 120, 150), labels=c(0, 30, 60, 90, 300, 600), line=0)
axis(1,c(0.5, 7.5),line=0,labels=c("",""), cex.axis=1.4)
text(c(1,2,3,4,5,6,7), -24, srt = 40, font=3, labels=c("Indica", "Aus/boro", "Basmati/sadri", "Intermediate", "Japonica", "Temperate jap", "Tropical jap"), xpd=TRUE, cex=1.4)
mtext("mPing", side=2, font=3, at=58, line=3, cex=1.4)
mtext("copy number", side=2, font=1, at=95, line=3, cex=1.4)

#break y
b <- 100
axis.break(2, b, style="slash")
#rect(-2, b, 2, b+2, border=FALSE, col='white')

#pvalue
pvalue(3, 80, 5.9, 146, 150, 3.4e-12)
segments(1, 80, 5, 80, col='black')
pvalue(6.1, 146, 7, 60, 150, 2.2e-16)

dev.off()

