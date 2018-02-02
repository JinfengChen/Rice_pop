library(pophelper)
setwd("~/Rice/Rice_population_sequence/Rice_3000/analysis/Introgression/ADMIXTURE")
qlist <- readQ("core_v0.7.pruneddata3.8.Q")
p <- plotQ(qlist, sortind= "all", showlegend = TRUE, returnplot=TRUE)
pdf("test.pdf")
p$plot
p$plot[[1]]
dev.off()
