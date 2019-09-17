# CRISPRCasFinder_scripts
Scripts for analysing CCF output files


## get_ccf_summary.py
This script will summarise the Crisprs_Report.tsv and Cas_Report.tsv output files from CRISPRCasFinder (CCF) from a group of genomes into a 3 output files.
For my uses, I give CCF output from genomes in the same clonal group (cg) so my file prefixes are cgXX_*.

Requirements:
 * Python3

Input: 
  * file paths to the Result_* directories made by CRISPRCasFinder
  
Outputs: 
  * cgXX_crispr_summary.csv
  * cgXX_cas_summary.csv
  * cgXX_crispr-cas_summary.csv
* See ccf_summary_example_output

N.B. This script assumes that the ```-cas``` option has been used when running CRISPRCasFinder. For input directories that do not have a Cas_Report.tsv their row in cgXX_cas_summary.csv will say "no cas files error".
