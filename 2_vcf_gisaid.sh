country=$(less country.txt) 

cpu=$(grep -c ^processor /proc/cpuinfo)
cpu_per=0.6
cpu_opt=$(echo "$cpu_per*$cpu/1" | bc)


tar xf hCoV-19_msa_*.tar.xz --wildcards 'msa_*/msa_*.fa*' -O | grep -A 1 ">.*/$country/.*/.*|.*|.*-.*-.*|.*" | awk 'length($0)>10'  > $country/$country.fasta 
mkdir -p $country/fasta
split -l60000 --numeric-suffixes=1 $country/$country.fasta $country/fasta/$country --additional-suffix=.fasta

rm $country/$country.fasta

mkdir -p tmp
export MAFFT_TMPDIR=$(pwd)/tmp

mkdir -p $country/mafft
mkdir -p $country/vcf_gisaid


fastas=$country/fasta/*
items_per_thread=1
while [ "${#fastas}" -gt "$(($items_per_thread*$cpu_opt))" ] #${#fastas[@]}
do
    items_per_thread=$((items_per_thread+1))
done

counter=0
command=""
echo 0 > gisaid_progress.txt
total=$(($(echo $country/fasta/* | wc -w)*2))

while [ $counter -le $total ]
do
	fastas2run=""
	for i in $(seq 1 $items_per_thread)
    do
        fastas2run="$fastas2run ${fastas[$counter]} "
		counter=$(($counter+1))
    done
  if [ ! "$fastas2run" == "" ]
  then
    command="$command bash vcf_gisaid.sh $fastas2run > out.log 2> err.log &"
  fi
done

eval " $command bash progress.sh $total 'paste -d+ gisaid_progress.txt| bc' "
wait

rm gisaid_progress.txt
rm -d tmp
rm -r $country/fasta
rm -r $country/mafft
rm out.log
rm err.log
echo all done