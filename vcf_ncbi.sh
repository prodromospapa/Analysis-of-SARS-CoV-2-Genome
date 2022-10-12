gatk='gatk-*/gatk --java-options' 

cpu=$(grep -c ^processor /proc/cpuinfo)
cpu_opt=$(echo "0.6*$cpu/1" | bc)

total_ram=$(grep MemTotal /proc/meminfo | awk '{print $2}')
total_ram_opt=$(echo "0.6*$total_ram/1" | bc)
ram=$(($total_ram_opt/$cpu_opt))

sras=$(wc -l < SraAccList/SraAccList_01.txt)
 
refseq="NC_045512.2"
country=$(less country.txt)
qual=30

shopt -s extglob #required for rm !()
counter=0
text_file=$1

cat $text_file | while read sra
do
	counter=$((counter+1))
	day=$(vdb-dump --info $sra | grep "TIME" | cut -d " " -f6 | sed 's/(//' | sed 's/\//_/g')
    if [ ! -f $country/vcf_ncbi/$day/$sra.vcf ]	
		then
		seq_tool=$(vdb-dump --info $sra | grep "platf" | cut -d " " -f4)
		seq_tool_name=$(echo $seq_tool | sed 's/SRA_PLATFORM_//')
		if [ $seq_tool_name = "ILLUMINA" ] || [ $seq_tool_name = "OXFORD_NANOPORE" ]
			then
			if [[  $day = [0-9]* ]] 
				then 
				prefetch $sra -O $country/vcf_ncbi/$day 2>/dev/null
				fastq-dump --stdout --accession $country/vcf_ncbi/$day/$sra > $country/vcf_ncbi/$day/$sra/$sra.fastq 2>/dev/null
				if [ $seq_tool_name = "ILLUMINA" ]
					then
					bwa mem -t 1 -M -R "@RG\tID:"$sra"\tLB:"$sra"\tPL:ILLUMINA\tPM:HISEQ\tSM:"$sra"" refseq/$refseq.fasta $country/vcf_ncbi/$day/$sra/$sra.fastq 2>/dev/null > vcf_ncbi/$day/$sra/$sra.sam 
					$gatk "-Xmx${ram}k" SortSam -I $country/vcf_ncbi/$day/$sra/$sra.sam -O $country/vcf_ncbi/$day/$sra/$sra.sorted.bam -SO coordinate > out.log 2> err.log
					$gatk "-Xmx${ram}k" CollectAlignmentSummaryMetrics -R refseq/$refseq.fasta -I $country/vcf_ncbi/$day/$sra/$sra.sorted.bam -O $country/vcf_ncbi/$day/$sra/$sra.alignment.metrics.txt > out.log 2> err.log
					$gatk "-Xmx${ram}k" MarkDuplicates -I $country/vcf_ncbi/$day/$sra/$sra.sorted.bam -O $country/vcf_ncbi/$day/$sra/calls_to_draft.bam -M $country/vcf_ncbi/$day/$sra/$sra.dupl.metrics.txt > out.log 2> err.log
				elif [ $seq_tool_name = "OXFORD_NANOPORE" ]
					then
					medaka_consensus -t 1 -i $country/vcf_ncbi/$day/$sra/$sra.fastq -d  refseq/$refseq.fasta -o $country/vcf_ncbi/$day/$sra > out.log 2> err.log					
				fi
			fi
		bcftools mpileup -Q $qual -d 100000 -a AD --skip-indels --fasta-ref refseq/$refseq.fasta $country/vcf_ncbi/$day/$sra/calls_to_draft.bam 2>/dev/null >  $country/vcf_ncbi/$day/$sra.vcf
		rm -r $country/vcf_ncbi/$day/$sra/
		fi
	fi
	if [ $text_file == "SraAccList/SraAccList_01.txt" ]
		then
		printf %.2f%%\\r "\r$(($counter*1000/$sras))e-1"
	fi
done

filename=${text_file%.*}
echo ${filename:22:22} done