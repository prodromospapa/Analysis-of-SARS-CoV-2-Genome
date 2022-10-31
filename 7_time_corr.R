suppressMessages(library("Hmisc"))
options(warn=-1)
country <- toString(read.table("country.txt"))[1]
file <- paste(country,"/correlation/annotation.csv",sep="")
data <- read.table(file,sep=",",header=TRUE,row.names=1,quote = "", stringsAsFactors = FALSE)

dates <- as.numeric(1:length(names(data)))

corre <- function(x){
return(rcorr(dates,as.numeric(x),type="pearson")$r[2,1])}

p <- function(x){
return(rcorr(dates,as.numeric(x),type="pearson")$P[2,1])}


corr_values <- round(apply(data,1,corre),2)
corr_p_values <- round(apply(data,1,p),2)

merged_table <- do.call(rbind, Map(data.frame, 'Correlation'=corr_values, 'P-values'=corr_p_values))
write.csv(merged_table,'time_corr.csv',row.names=TRUE)
print('all done')
