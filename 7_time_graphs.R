#country <- toString(read.table("country.txt"))[1]
country <- "Greece"
file <- paste(country,"/correlation/annotation.csv",sep="")
data <- read.table(file,sep=",",header=TRUE,row.names=1,quote = "", stringsAsFactors = FALSE)

dates= as.Date(gsub("^X", "", colnames(data)),"%m_%d_%Y")
system(paste("mkdir -p ",country,"/correlation/graphs",sep=""))
for (orf in row.names(data)){
    png(file=paste(country,"/correlation/graphs/",orf,".png", sep = ""))
    plot(dates, data[orf,],main = orf,xlab='dates',ylab='frequencies')
    dev.off()
}