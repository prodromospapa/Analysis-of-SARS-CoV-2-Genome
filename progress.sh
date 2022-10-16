country=$1
total=$2
counter=$3
while [ $counter -le $total ]
    do
    counter=$3
    printf %.2f%%\\r "$(($counter*1000/$total))e-1"
done