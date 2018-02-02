library(pophelper)
setwd("~/Rice/Rice_population_sequence/Rice_3000/analysis/Introgression/ADMIXTURE")
sfiles <- list.files(path=".", pattern=".Q.reordered.txt")
qlists <- readQ(files=sfiles)
plotQ(qlists,imgoutput="join", sortind="all", showlegend=TRUE, sharedindlab=FALSE, imgtype = "pdf", height = 2, width = 10, outputfilename = 'multi_run_plot', grplab=c('test', 'test1'))

