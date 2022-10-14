#install minoconda manually
#https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
#https://docs.conda.io/en/latest/miniconda.html

#install medaka
if [ ! "$(conda env list | grep thesis)" ]
then
    conda create -y -n thesis >/dev/null 2>&1
fi

conda activate thesis

#install bash software
conda install -n thesis -y -c conda-forge python >/dev/null 2>&1
conda install -n thesis -y -c bioconda -c conda-forge medaka >/dev/null 2>&1
conda install -n thesis -y -c conda-forge unzip >/dev/null 2>&1
conda install -n thesis -y -c bioconda sra-tools >/dev/null 2>&1
conda install -n thesis -y -c bioconda mafft >/dev/null 2>&1
conda install -n thesis -y -c bioconda bwa >/dev/null 2>&1
conda install -n thesis -y -c bioconda bcftools >/dev/null 2>&1
conda install -n thesis -y -c bioconda snp-sites >/dev/null 2>&1
conda install -n thesis -y -c bioconda entrez-direct >/dev/null 2>&1
conda install -n thesis -y -c bioconda samtools >/dev/null 2>&1

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



#install python libraries
conda install -n thesis --file requirements.txt >/dev/null 2>&1
#conda install pip --file requirements.txt >/dev/null 2>&1


#install R libraries
Rscript -e 'install.packages("gplots")' >/dev/null 2>&1