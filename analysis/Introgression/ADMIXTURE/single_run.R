library(pophelper)
setwd("~/Rice/Rice_population_sequence/Rice_3000/analysis/Introgression/fastStructure")
qlist <- readQ("K5/testoutput_simple.5.meanQ")
plotQ(qlist, sortind= "all", showlegend = TRUE)

