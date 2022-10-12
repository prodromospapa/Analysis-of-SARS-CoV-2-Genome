# thesis
prerequirements: 1)all .sh must be run with 'bash *.sh' format
                 2)Anaconda/minoconda must be installed in the system
                 3)Access to a sudo user is obligated if you run it for the first time in order to install the needed software using the 0_install_requirements.sh.sh      

It is recommended to run in a tmux session as most of the scripts may run for a long period of time.

1)Run 0_install_requirements.sh if you use this project for the first time and everything that is needed will be downloaded automatically.
2)Run 1_vcf_ncbi.sh using 'source' instead of 'bash' in front of the shell script otherwise it won't run properly
3)Run 2_gisaid_ncbi.sh
4)Run 4_fisher.sh
5)Run 5_annotation.py
6)Run 6_heatmap.R

After you have run all of the above you can find the heatmap graph in the heatmap folder named heatmap.pdf
