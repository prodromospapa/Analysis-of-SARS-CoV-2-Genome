country=$(less country.txt)
total=$(find $country/vcf_ncbi/*/*.vcf | wc -l)
counter=$(find $country/p_tables/*/*.csv | wc -l)
command="bash progress.sh $country $total $counter & "

for text in $country/SraAccList/*
do 
    command="$command python3 fisher.py $text &"
done

eval " ${command::-2} "

wait
echo done