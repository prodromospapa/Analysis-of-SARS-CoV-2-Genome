suppressMessages(library("gplots"))
options(warn=-1)
country <- toString(read.table("country.txt"))[1]

data <- read.table(paste(country,"/heatmap/heatmap.csv",sep=""),sep=",",header=TRUE,row.names=1,quote = "", stringsAsFactors = FALSE)
colnames(data) <- as.Date(gsub("^X", "", colnames(data)),tryFormats = c("%m_%d_%Y"))

pdf(file=paste(country,"/",country,".pdf",sep=""))
heatmap.2(as.matrix(data),
    scale="row", 
    key=T, 
    keysize=1,
    density.info="none", 
    trace="none",
    dendogram='none',
    Rowv=NULL,
    Colv=NULL)
garbage <- dev.off()