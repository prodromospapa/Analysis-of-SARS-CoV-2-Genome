country=$(less country.txt)
total=$(find $country/vcf_ncbi/*/*.vcf | wc -l)
counter="find ${country}/p_tables/*/*.csv | wc -l"
command=""

for text in $country/SraAccList/*
do 
    command="$command python3 fisher.py $text &"
done

eval " $command bash progress.sh $total $counter "

wait
echo done