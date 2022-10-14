country=$1
total=$2
counter=$(find $3 | wc -l)
while [ $counter -le $total ]
    do
    counter=$(find $3 | wc -l)
    printf %.2f%%\\r "$(($counter*1000/$total))e-1"
done