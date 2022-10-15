#install minoconda manually
#https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html
#https://docs.conda.io/en/latest/miniconda.html

conda deactivate

#install python libraries
pip install -r requirements.txt >/dev/null 2>&1

#install R libraries
Rscript -e 'install.packages("gplots")' >/dev/null 2>&1

#install medaka
if [[ ! $(conda env list | grep thesis) ]]
then
    conda create -y -n thesis >/dev/null 2>&1
fi

conda activate thesis 

#install bash software
cat conda.txt | while read lib
    do
    lib_name=$(echo $lib | rev |cut -d ' ' -f 1 | rev)
    if [[ $(conda list -n thesis $lib_name | wc -l) -eq 3 ]]
    then
        conda install -n thesis -y -c $lib >/dev/null 2>&1
    fi
done

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
    if [[ $(ver $currentver) -lt $(ver $requiredver) ]]
    then
        rm -r gatk-*
        wget -q $url
        unzip -qq gatk-*.zip
        rm gatk-*.zip
    fi
fi


echo all done