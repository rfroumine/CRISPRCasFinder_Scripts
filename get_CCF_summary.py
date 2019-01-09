#!/usr/bin/env python3
#
# Get details about CRISPR arrays from Crisprs_REPORT files
#
# To run: 
# module load python/3.6.6-gcc5
# python3 get_CCF_summary.py --crispr_input crisprSummary_2018_12_03_16_07_02.csv --cas_input casSummary_2018_12_04_13_54_02.csv
#
# Authors - Roni Froumine

import time
import string, re
import os, sys
import csv
from collections import defaultdict
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


    parser.add_argument("--crispr_input", nargs=1, required=True, help="crispr ccf summary")
    parser.add_argument("--cas_input", nargs=1, required=True, help="cas ccf summary")
    
    return parser.parse_args()

def main():

    # get arguments
    args = get_arguments()

    # create output file with header
    currTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    outputFileName = "ccfSummary_" + currTime + ".csv"

    ccfSummary = open(outputFileName, "w")
    writer = csv.writer(ccfSummary)
    writer.writerow(["Genome", "num_CRISPR_Ev3or4", "Cas_TypeIE_atleast5genes", "Else"])

    for filepath in args.crispr_input:
        crisprSummary = open(filepath)
        crisprdata = csv.reader(crisprSummary)
        header = next(crisprdata)

    for filepath in args.cas_input:
        casSummary = open(filepath)
        casdata = csv.reader(casSummary)
        header = next(casdata)

    output_dict = defaultdict(list)
    for row1 in crisprdata:
        genome = row1[0]
        if int(row1[-1]) >= 3:
            if genome not in output_dict:
                output_dict[genome].append(1)
            else:
                output_dict[genome][0] += 1
        if genome not in output_dict:
            output_dict[genome].append(0)

    for row2 in casdata:
        genome = row2[0]
        cc_type = row2[1]
        cas_genes = row2[-1]
        if len(cas_genes.split(";")) >=5 and not cc_type == "CAS":
            output_dict[genome].append(cc_type)

    output_rows = []
    for genome, details in output_dict.items():
        output_rows.append([genome, *details])

    writer.writerows(output_rows)
    ccfSummary.close()

if __name__ == "__main__":
    main()
