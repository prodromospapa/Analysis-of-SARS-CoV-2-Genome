total=$1
count=$(eval $2 2>/dev/null)
while [ "$count" -lt "$total" ]
    do
    if [[ $count =~ ^[0-9]+$ ]]
    then
        error=$count
    fi
    count=$(eval $2 2>/dev/null)
    if ! [[ $count =~ ^[0-9]+$ ]]
    then
        count=$error
    fi
    printf %.2f%%\\r "$(($count*10000/$total))e-2"
done