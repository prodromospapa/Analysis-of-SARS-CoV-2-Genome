#install minoconda manually
#https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html

function ver { printf "%03d%03d%03d%03d" $(echo "$1" | tr '.' ' '); }

#download latest gatk
url=$(curl -s https://github.com/broadinstitute/gatk/releases \
    | grep "gatk-.*.zip" \
    | cut -d : -f 2,3 \
    | tr -d \" \
    | head -n 1 \
    | sed 's/<\/strong> <a href=\(.*\)>gatk-\(.*\).zip<\/a><br>/\1/')
if [ ! -d gatk-* ]
then
    wget -q $url
    unzip -qq gatk-*.zip
    rm gatk-*.zip
else
    currentver=$(find gatk-*/ | head -1 | cut -d \- -f 2 | sed 's/\///')
    requiredver=$(echo $url | cut -d / -f 8)
    if [ $(ver $currentver) -lt $(ver $requiredver) ]
    then
        rm -r gatk-*
        wget -q $url
        unzip -qq gatk-*.zip
        rm gatk-*.zip
    fi
fi


#install bash software
sudo apt-get install -y sra-toolkit >/dev/null 2>&1
sudo apt-get install -y mafft >/dev/null 2>&1
sudo apt-get install -y bwa >/dev/null 2>&1
sudo apt-get install -y bcftools >/dev/null 2>&1
sudo apt-get install -y snp-sites >/dev/null 2>&1
sudo apt-get install -y ncbi-entrez-direct >/dev/null 2>&1
sudo apt-get install -y samtools >/dev/null 2>&1
sudo apt-get install -y bwa >/dev/null 2>&1
#here it can be changed to anaconda install for no sudo users

#install medaka
if [ ! "$(conda env list | grep medaka)" ]
then
    conda create -n medaka -c conda-forge -c bioconda medaka
fi

#install python libraries
pip install -r requirements.txt >/dev/null 2>&1
#conda install pip --file requirements.txt >/dev/null 2>&1


#install R libraries
Rscript -e 'install.packages("gplots")' >/dev/null 2>&1