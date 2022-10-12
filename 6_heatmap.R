library("gplots")
options(warn=-1)
country <- toString(read.table("country.txt"))[1]

data <- read.table(paste(country,"/heatmap/heatmap.csv",sep=""),sep=",",header=TRUE,row.names=1,quote = "", stringsAsFactors = FALSE)
colnames(data) <- as.Date(gsub("^X", "", colnames(data)),tryFormats = c("%m_%d_%Y"))

m <- as.matrix(data)
pdf(file=paste(country,".pdf",sep=""))
heatmap.2(m,dendogram='none',scale='row',Rowv=NULL,Colv=NULL)
dev.off()