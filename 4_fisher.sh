country=$(less country.txt)
total=$(find $country/vcf_ncbi/*/*.vcf | wc -l)
counter=$country/p_tables/*/*.csv
command="bash progress.sh $country $total $counter & "
for text in $country/SraAccList/*
do 
    command="$command python3 fisher.py $text &"
done

eval " ${command::-2} "

wait
echo done