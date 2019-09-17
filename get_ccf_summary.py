#!/usr/bin/env python3
#
# Use this script to summarise CRISPRCasFinder (CCF) output from many genomes into one list.
# Input: file paths to the Result_* directories made by CRISPRCasFinder
# Output: cgXX_crispr_summary.csv, cgXX_cas_summary.csv, cgXX_crispr-cas_summary.csv
#
# To run: 
# module load python/3.6.6-gcc5 
# python3 get_ccf_summary.py --input/projects/js66/individuals/roni/CCF_output/CG23_CCF_output/*_output/R*
#
# Authors - Roni Froumine

#import time
import string, re
#import os, sys
import csv
from argparse import ArgumentParser
import json
from pathlib import Path
from collections import defaultdict

#from holtlib import job_scheduler, env_modules

def get_arguments():
    parser = ArgumentParser(description="extract summary information from CRISPRCasFinder output")

    # job submission options
    #parser.add_argument('--walltime', required=False, default='0-1:00:00', help='Time for job (default 1 hour; 0-1:00:00)')
    #parser.add_argument('--cpus', required=False, default='1', help='CPUs for job (default1)')
    #parser.add_argument('--memory', required=False, default='2048', help='Memory for job (default 2048)')

    #parser.add_argument('--compute', required=False,default = 'massive', help='Compute to use')
    #parser.add_argument('--partition', required=False, help='Partition to use')


    parser.add_argument("--input", nargs="+", required=True, help="paths to the Result_* directories made by CRISPRCasFinder")
    
    return parser.parse_args()

def main():

    # get arguments
    args = get_arguments()

    # prepare output files
    ## prefix for output files
    cg_name = re.findall(r"(?:CG|ST)\d+", args.input[0])[0].lower()
    ## crispr output 
    crispr_filename = f"{cg_name}_crispr_summary.csv"
    crispr_ofile = open(crispr_filename, "w")
    crispr_writer = csv.writer(crispr_ofile)
    crispr_writer.writerow(["Genome", "CRISPR_Id", "CRISPR_Start", "CRISPR_End", "Consensus_Repeat", "Repeat_Length", "Spacers_Nb", "Mean_Size_Spacers",  "Repeats_Conservation(percent_id)", "Evidence_Level"])
    ## cas output
    cas_filename = f"{cg_name}_cas_summary.csv"
    cas_ofile = open(cas_filename, "w")
    cas_writer = csv.writer(cas_ofile)
    cas_writer.writerow(["Genome", "System_Type", "Begin_and_End", "Seq_ID", "Cas_Genes"])
    ## crispr-cas output
    cc_filename = f"{cg_name}_crispr-cas_summary.csv"
    cc_ofile = open(cc_filename, "w")
    cc_writer = csv.writer(cc_ofile)
    cc_writer.writerow(["Genome", "Num_CRISPR(Ev3or4)", "CC_Type", "Cas_Genes"])
    
    # loop through input_fps 
    for input_fp in args.input:
        filepath = Path(input_fp)

        # get correct genome name from the command part in the result.json file
        json_fp = filepath / "result.json"
        with json_fp.open("r") as fh:
            input_data = json.loads(fh.read())
            date, version, command, contigs_data = input_data.values()
            genome_name = command.split("/")[-1].split(".fasta")[0]

        # create a summary from the CRISPR_Reports for each genome
        # sometimes the -cas option isn't used or causes error so some genomes do not have a cas_REPORT so using try and except
        crispr_fp = filepath / "TSV" / "Crisprs_REPORT.tsv"
        try:
            crisprs_report = open(crispr_fp)
            crispr_data = csv.reader(crisprs_report, delimiter='\t')
            header = next(crispr_data)
            crispr_rows = []

            for row in crispr_data:
                if not row == []:
                    crispr_rows.append([genome_name, row[4], row[5], row[6], row[10], row[13], row[14], row[15], row[19], row[26]])
            crispr_writer.writerows(crispr_rows)

            # create a summary from the Cas_Reports for each genome
            cas_fp = filepath / "TSV" / "Cas_REPORT.tsv"
            cas_report = open(cas_fp)
            cas_data = csv.reader(cas_report, delimiter='\t')
            header = next(cas_data)

            cas_system_summaries = []
            while True:
                try:
                    row = next(cas_data)
                except StopIteration:
                    break
                if row:
                    if row[0].startswith('####Summary'):
                        cas_system_summaries.append(row[0]) 

            cas_rows = []
            for system_summary in cas_system_summaries:
                system_summary_split_list = [genome_name] + system_summary.replace("####Summary system ", ":").split(":")[1:]

                cas_rows.append(system_summary_split_list) 

        except FileNotFoundError:
            alt_row = [genome_name] + ["no"] + ["cas"] + ["files"] + ["error"]
            cas_rows.append(alt_row)

        cas_writer.writerows(cas_rows)

    crispr_ofile.close()        
    cas_ofile.close()

    # create a less detailed summary of the crispr and cas outputs just made
    crispr_sum = open(crispr_filename, "r")
    crispr_sum_data = csv.reader(crispr_sum)
    header = next(crispr_sum_data)

    cas_sum = open(cas_filename, "r")
    cas_sum_data = csv.reader(cas_sum)
    header = next(cas_sum_data)

    output_dict = defaultdict(list)
    for row1 in crispr_sum_data:
        genome = row1[0]
        # only want crispr with evidence 3 or 4
        if int(row1[-1]) >= 3:
            if genome not in output_dict:
                output_dict[genome].append(1)
            else:
                output_dict[genome][0] += 1
        if genome not in output_dict:
            output_dict[genome].append(0)

    for row2 in cas_sum_data:
        genome = row2[0]
        cc_type = row2[1]
        cas_genes = row2[-1]
        if cc_type != "CAS" and cc_type != "no":
            output_dict[genome].append(cc_type)
            output_dict[genome].append(cas_genes)

    output_rows = []
    for genome, cc_details in output_dict.items():
        output_rows.append([genome, *cc_details])

    cc_writer.writerows(output_rows)
    cc_ofile.close()


if __name__ == "__main__":
    main()
