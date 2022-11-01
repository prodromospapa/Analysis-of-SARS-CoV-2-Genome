suppressMessages(library("Hmisc"))
options(warn=-1)
country <- toString(read.table("country.txt"))[1]
file <- paste(country,"/correlation/correlation.csv",sep="")
data <- read.table(file,sep=",", header=TRUE,row.names=1, quote = "", stringsAsFactors = FALSE)

dates <- as.numeric(1:length(names(data)))
corre <- function(x){
return(rcorr(dates,as.numeric(x),type="pearson")$r[2,1])}

p <- function(x){
return(rcorr(dates,as.numeric(x),type="pearson")$P[2,1])}


corr_values <- round(apply(data,1,corre),2)
corr_p_values <- round(apply(data,1,p),2)

merged_table <- do.call(rbind, Map(data.frame, 'Correlation'=corr_values, 'P-values'=corr_p_values))
write.csv(merged_table,paste(country,'/time_corr.csv',sep=""),row.names=TRUE)

dates= as.Date(gsub("^X", "", colnames(data)),"%m_%d_%Y")
system(paste("mkdir -p ",country,"/correlation/graphs",sep=""))
for (orf in row.names(data)){
    png(file=paste(country,"/correlation/graphs/",orf,".png", sep = ""))
    plot(dates, data[orf,],main = orf,xlab='dates',ylab='frequencies')
    dev.off()
}

cat('all done\n')
