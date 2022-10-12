command=""
for text in $country/SraAccList/*
do 
    command="$command python3 fisher.py $text &"
done

eval " ${command::-2} "

wait
echo done