#!/usr/bin/env python3
#
# Get details about CRISPR arrays from Crisprs_REPORT files
#
# To run: 
# module load python/3.6.6-gcc5
# python3 get_CCF_CRISPR_summary.py —input cg23_ccf_output/*_output/R*/TSV/Crisprs_REPORT.tsv
#
# Authors - Roni Froumine

import time
import string, re
import os, sys
import csv
import datetime
from argparse import ArgumentParser

from holtlib import job_scheduler, env_modules

def get_arguments():
    parser = ArgumentParser(description="Navo through CCF practice")

    # job submission options
    parser.add_argument('--walltime', required=False, default='0-1:00:00', help='Time for job (default 1 hour; 0-1:00:00)')
    parser.add_argument('--cpus', required=False, default='1', help='CPUs for job (default1)')
    parser.add_argument('--memory', required=False, default='2048', help='Memory for job (default 2048)')

    parser.add_argument('--compute', required=False,default = 'massive', help='Compute to use')
    parser.add_argument('--partition', required=False, help='Partition to use')


    parser.add_argument("--input", nargs="+", required=True, help="List of assembly inputs")
    
    return parser.parse_args()

def main():

    # get arguments
    args = get_arguments()

    # create output file with header
    currTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    outputFileName = "crisprSummary_" + currTime + ".csv"

    crisprSummary = open(outputFileName, "w")
    writer = csv.writer(crisprSummary)
    writer.writerow(["Genome", "CRISPR_Id", "CRISPR_Start", "CRISPR_End", "Consensus_Repeat", "Repeat_Length", "Spacers_Nb", "Mean_size_Spacers",  "Repeats_Conservation(percent_idenity)", "Evidence_Level"])

    # get wanted info from individual Crisprs_REPORT files and add them to the output file
    for filepath in args.input:
    
        genome_name = filepath.split('/')[1].split('.fasta')[0]

        crisprs_report = open(filepath)
        data = csv.reader(crisprs_report, delimiter='\t')
        header = next(data)
        crisprSummary_rows = []
        for row in data:
            if not row == []:
                crisprSummary_rows.append([genome_name, row[4], row[5], row[6], row[10], row[13], row[14], row[15], row[19], row[26]])
        writer.writerows(crisprSummary_rows)

    crisprSummary.close()

if __name__ == "__main__":
    main()
