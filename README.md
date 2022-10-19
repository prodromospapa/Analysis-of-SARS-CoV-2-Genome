Instructions
======

prerequirements: 1)R and python must be installed in the system
                 2)Anaconda/miniconda must be installed in the system
                 3)Academic email to download GISAID msa file

It is recommended to run in a tmux session as most of the scripts may run for a long period of time.

* Run 0_install_requirements.sh if you use this project for the first time and everything that is needed will be downloaded automatically. It must be run using 'source' instead of
* Run 1_vcf_ncbi.sh using 'source' instead of 'bash' in front of the shell script otherwise it won't run properly
* Run 2_gisaid_ncbi.sh using 'bash'
* Run 4_fisher.sh using 'bash'
* Run 5_annotation.py using 'python3'
* Run 6_heatmap.R using 'Rscript'

After you have run all of the above you can find the heatmap graph in the country folder named after the country name
