country=$(less country.txt)
sralist=https://www.ncbi.nlm.nih.gov/sra/?term=txid2697049%5BOrganism%3Anoexp%5D+NOT+0%5BMbases%5D+AND+$country

gatk='gatk-4.2.6.1/gatk --java-options' 
cpu=$(grep -c ^processor /proc/cpuinfo)
cpu_opt=$(echo "0.6*$cpu/1" | bc)


if [ ! -d "$country/SraAccList" ]
then
    while [ ! -f "SraAccList.txt" ]
    do
        echo -ne $sralist'\r'
    done
    sed -i '/^$/d' SraAccList.txt
    sras=$(wc -l < SraAccList.txt)
    rounded="$((($sras / 1000 + 1) *1000))"
    lines=$(($rounded/$cpu_opt))
    mkdir -p $country/SraAccList
    split -l $lines --numeric-suffixes=1 SraAccList.txt $country/SraAccList/SraAccList_ --additional-suffix=.txt
    rm SraAccList.txt
fi

if [ ! -f "refseq/NC_045512.2.fasta" ]
then
    refseq="NC_045512.2"
    ram=15
    esearch -db nucleotide -query "${refseq}" | efetch -format fasta > refseq/$refseq.fasta
    bwa index refseq/$refseq.fasta refseq >/dev/null &> /dev/null
    samtools faidx refseq/$refseq.fasta refseq &> /dev/null
    $gatk "-Xmx${ram}G" CreateSequenceDictionary -R refseq/$refseq.fasta -O refseq/$refseq.dict &> /dev/null
fi

counda activate thesis

command=""

for text in $country/SraAccList/*
do 
    command="$command bash vcf_ncbi.sh $text &"
done

eval " ${command::-2} "

wait
rm out.log
rm err.log
echo all done 