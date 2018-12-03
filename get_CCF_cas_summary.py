#!/usr/bin/env python3
#
# Get details about Cas genes from Cas_REPORT files
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
    outputFileName = "casSummary_" + currTime + ".csv"

    casSummary = open(outputFileName, "w")
    writer = csv.writer(casSummary)
    writer.writerow(["Genome", "System_type", "Begin_and_End", "seq_ID", "cas_genes"])

    # get wanted info from individual Crisprs_REPORT files and add them to the output file
    for filepath in args.input:
    
        genome_name = filepath.split('/')[1].split('.fasta')[0]

        cas_report = open(filepath)
        data = csv.reader(cas_report, delimiter='\t')
        header = next(data)
        
        cas_system_summaries = []
        while True:
            try:
                row = next(data)
            except StopIteration:
                break
            if row:
                if row[0].startswith('####Summary'):
                    cas_system_summaries.append(row[0])

        casSummary_rows = []
        for system_summary in cas_system_summaries:
            system_summary_split_list = [genome_name] + system_summary.replace("####Summary system ", ":").split(":")[1:]
            casSummary_rows.append(system_summary_split_list)


        writer.writerows(casSummary_rows)

    casSummary.close()

if __name__ == "__main__":
    main()
