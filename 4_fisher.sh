country=$(less country.txt)
total=$(find $country/vcf_ncbi/*/*.vcf | wc -l)
command=""

for text in $country/SraAccList/*
do 
    number=$(echo $text | rev | cut -c1-6 | rev | cut -c1-2)
    echo 0 > fisher_progress_$number.txt
    command="$command python3 fisher.py $text $number &"
done

eval " $command bash progress.sh $total 'paste -d+ fisher_progress_*.txt| bc' "

wait
rm fisher_progress_*.txt
echo all done