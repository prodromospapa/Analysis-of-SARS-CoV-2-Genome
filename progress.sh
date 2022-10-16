total=$1
count=$(eval $2)
while [ "$count" -lt "$total" ]
    do
    if [[ $count =~ ^[0-9]+$ ]]
    then
        error=$count
    fi
    count=$(eval $2)
    if ! [[ $count =~ ^[0-9]+$ ]]
    then
        count=$error
    fi
    printf %.2f%%\\r "$(($count*1000/$total))e-1"
done