# CRISPRCasFinder_scripts
Scripts for analysing CCF output files


## get_ccf_summary.py
This script will summarise CRISPRCasFinder (CCF) output from group of genomes into a few output files.
For my uses, I give CCF output from genomes in the same clonal group (cg) so my file prefixes are cgXX_*.
Input: 
  * file paths to the Result_* directories made by CRISPRCasFinder
Outputs: 
  * cgXX_crispr_summary.csv
  * cgXX_cas_summary.csv
  * cgXX_crispr-cas_summary.csv
See example_output
