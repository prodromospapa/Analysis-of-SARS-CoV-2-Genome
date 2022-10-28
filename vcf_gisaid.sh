country=$(less country.txt)
refseq="EPI_ISL_402124"
fastas=$@

for fasta in $fastas
do
    counter=$(echo $fasta | sed "s/$country\/fasta\/$country//g" | sed 's/.fasta//g')
    mafft --6merpair --thread -1 --keeplength --addfragments $fasta refseq/$refseq.fasta > $country/mafft/$country.$counter.mafft.fasta
    echo $(($(less gisaid_progress.txt)+1)) > gisaid_progress.txt 
    snp-sites $country/mafft/$country.$counter.mafft.fasta -v > $country/vcf_gisaid/$country.$counter.vcf
    echo $(($(less gisaid_progress.txt)+1)) > gisaid_progress.txt 
done