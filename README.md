Instructions
======

Prerequirements
----------------

* Python must be installed in the system
* Anaconda/miniconda must be installed in the system
* Academic email to download GISAID msa file

It is recommended to run in a tmux session as most of the scripts may run for a long period of time.

* Run 0_install_requirements.sh if you are using this project for the first time and everything that is needed will be downloaded automatically. It must be run using 'source'
* Run 1_vcf_ncbi.sh using 'source' otherwise it won't run properly
* Run 2_gisaid_ncbi.sh using 'bash'
* Run 4_chi.sh using 'bash'
* Run 5_heatmap.py using 'python3'

After that you can find the heatmap graph in the country folder named after the country name in the directory

* Run 6_correlation.py using 'python3'
* run 7_time_corr.R using 'Rscript'

After that you can find in 'correlation' folder:
* Graphs of dates-percentage of difference between reference sequence and samples
* Table with percentage of difference for each gene in time
* Table with correlation value for each gene
