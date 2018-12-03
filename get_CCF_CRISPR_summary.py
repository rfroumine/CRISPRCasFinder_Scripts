#!/usr/bin/env python3
#
# Practicing navo through CCF files
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

    # Get arguments
    args = get_arguments()

    currTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    outputFileName = "crisprSummary_" + currTime + ".csv"

    crisprSummary = open(outputFileName, "w")
    writer = csv.writer(crisprSummary)
    writer.writerow(["Genome", "CRISPRId", "NbRepeats", "EvidenceLevel"])

    for filepath in args.input:
    
        filename = filepath.split('/')[1].split('.fasta')[0]

        crisprs_report = open(filepath)
        data = csv.reader(crisprs_report, delimiter='\t')
        header = next(data)
        crisprSummary_rows = []
        for row in data:
            if not row == []:
                crisprSummary_rows.append([filename, row[4], row[17], row[26]])
        writer.writerows(crisprSummary_rows)

    crisprSummary.close()

if __name__ == "__main__":
    main()