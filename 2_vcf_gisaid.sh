country=$(less country.txt) 
refseq="EPI_ISL_402124"

cpu=$(grep -c ^processor /proc/cpuinfo)
cpu_per=0.6
cpu_opt=$(echo "$cpu_per*$cpu/1" | bc)

path=$(pwd)

tar xf hCoV-19_msa_*.tar.xz --wildcards 'msa_*/msa_*.fa*' -O | grep -A 1 ">.*/$country/.*/.*|.*|.*-.*-.*|.*" | awk 'length($0)>10'  > $country/$country.fasta 
mkdir -p $country/fasta
split -l60000 --numeric-suffixes=1 $country/$country.fasta $country/fasta/$country --additional-suffix=.fasta

rm $country/$country.fasta

mkdir -p tmp
export MAFFT_TMPDIR="$path/tmp"

mkdir -p $country/mafft
mkdir -p $country/vcf_gisaid

counter=0
total="$(ls $country/fasta | wc -l)"
for fasta in $country/fasta/*
do	
	counter=$((counter+1))
	mafft --6merpair --thread -$cpu_opt --keeplength --addfragments $fasta refseq/$refseq.fasta > $country/mafft/$country.$counter.mafft.fasta
	snp-sites $country/mafft/$country.$counter.mafft.fasta -v > $country/vcf_gisaid/$country.$counter.vcf
	printf %.2f%%\\r "\r$(($counter*1000/$total))e-1"
done
rm -d tmp
rm -r $country/fasta
rm -r $country/mafft
echo all done