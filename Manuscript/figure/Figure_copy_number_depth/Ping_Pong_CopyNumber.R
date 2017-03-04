plot_correlation <- function(x, y, xlab, ylab, xmin, xmax, ymin, ymax, title, ...){
    plot(x, y, xlab= xlab, ylab= ylab, main= title, xlim=c(xmin, xmax), ylim=c(ymin, ymax))
    #regression line
    abline(lm(y~x), col="red")
    reg <- lm(y~x)
    a <- round(reg$coefficients[[2]], 2)
    b <- round(reg$coefficients[[1]], 2)
    text(0, 12, pos=4, paste('Y = ', b, '+', paste(a, 'X', sep=''), sep=' '), cex=1)
    #corrlation
    cor <- cor.test(x, y)
    r2 <- round(cor$estimate[[1]], 2)
    p  <- cor$p.value
    if (p == 0){
        p = '2.2e-16'
    }else{
        p = signif(p, 2) 
    }
    text(0, 13, pos=4, paste('R-squared =', r2, ', p-value <', p, sep=' '), cex=1) 
}

pdf('Ping_Pong_CopyNumber.pdf')
x <- read.table("Ping_Pong_CopyNumber.txt", header=F)
ping_relocate2 = x[,3]
pong_relocate2 = x[,4]
ping_depth     = x[,5]
pong_depth     = x[,6]

plot_correlation(ping_relocate2, ping_depth, 'Ping Copy Number by RelocaTE2', 'Ping Copy Number by read depth', 0, 5, 0, 5, 'Default')
plot_correlation(pong_relocate2, pong_depth, 'Pong Copy Number by RelocaTE2', 'Pong Copy Number by read depth', 0, 20, 0, 20, 'Default')

dev.off()
