gatk='gatk-*/gatk --java-options' 

refseq="NC_045512"
country=$(less country.txt)
qual=20

cpu_opt=$(find $country/SraAccList/* | wc -l)
total_ram=$(grep MemTotal /proc/meminfo | awk '{print $2}')
ram_per=0.6
total_ram_opt=$(echo "$ram_per*$total_ram/1" | bc)
ram=$(($total_ram_opt/$cpu_opt))

shopt -s extglob #required for rm !()
counter=0
text_file=$1
file_number=$(echo ${text_file%.*} | tail -c3)

cat $text_file | while read sra
do
	counter=$((counter+1))
	info=$(vdb-dump --info $sra)
	day=$(echo "$info" | grep "TIME" | cut -d " " -f6 | sed 's/(//' | sed 's/\//_/g')
    if [ ! -f $country/vcf_ncbi/$day/$sra.vcf ]	
		then
		seq_tool=$(echo "$info" | grep "platf" | cut -d " " -f4)
		seq_tool_name=$(echo $seq_tool | sed 's/SRA_PLATFORM_//')
		if [ $seq_tool_name = "ILLUMINA" ] || [ $seq_tool_name = "OXFORD_NANOPORE" ]
			then
			if [[  $day = [0-9]* ]] 
				then 
				prefetch $sra -O $country/vcf_ncbi/$day 
				fastq-dump --stdout --accession $country/vcf_ncbi/$day/$sra > $country/vcf_ncbi/$day/$sra/$sra.fastq 
				if [ $seq_tool_name = "ILLUMINA" ]
					then
					bwa mem -t 1 -M -R "@RG\tID:"$sra"\tLB:"$sra"\tPL:ILLUMINA\tPM:HISEQ\tSM:"$sra"" refseq/$refseq.fasta $country/vcf_ncbi/$day/$sra/$sra.fastq  > $country/vcf_ncbi/$day/$sra/$sra.sam 
					$gatk "-Xmx${ram}k" SortSam -I $country/vcf_ncbi/$day/$sra/$sra.sam -O $country/vcf_ncbi/$day/$sra/$sra.sorted.bam -SO coordinate 
					$gatk "-Xmx${ram}k" CollectAlignmentSummaryMetrics -R refseq/$refseq.fasta -I $country/vcf_ncbi/$day/$sra/$sra.sorted.bam -O $country/vcf_ncbi/$day/$sra/$sra.alignment.metrics.txt 
					$gatk "-Xmx${ram}k" MarkDuplicates -I $country/vcf_ncbi/$day/$sra/$sra.sorted.bam -O $country/vcf_ncbi/$day/$sra/calls_to_draft.bam -M $country/vcf_ncbi/$day/$sra/$sra.dupl.metrics.txt 
				elif [ $seq_tool_name = "OXFORD_NANOPORE" ]
					then
					medaka_consensus -t 1 -i $country/vcf_ncbi/$day/$sra/$sra.fastq -d  refseq/$refseq.fasta -o $country/vcf_ncbi/$day/$sra 					
				fi
			fi
		bcftools mpileup -Q $qual -d 100000 -a AD --skip-indels --fasta-ref refseq/$refseq.fasta $country/vcf_ncbi/$day/$sra/calls_to_draft.bam  >  $country/vcf_ncbi/$day/$sra.vcf
		rm -r $country/vcf_ncbi/$day/$sra/
		fi
	fi
	echo $counter > ncbi_progress_$file_number.txt
done

echo $file_number done