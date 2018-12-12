#!/usr/bin/env python
#
# Submit multiple CRISPRCasFinder jobs to SLURM (input = assembly files)
#
# Authors - Roni Froumine, Kelly Wyres
#
# Dependencies: - prob can remove this
#    loads CRISPRCasFinder/4.2.17
#    loads python
#
# Example command on merri:
'''
module load python/3.6.6-gcc5
python /vlsci/SG0006/shared/code/holtlab/runCRISPRCasFinder_SLURM.py --input /your/dir/ 
'''
#
# Last modified - Dec 12, 2018
# Changes:
#  
import string, re
import os, sys
from argparse import ArgumentParser
from Bio import SeqIO
import time

from holtlib import job_scheduler, env_modules


def parse_args():

    parser = ArgumentParser(description="Submits CRISPRCasFinder jobs to Slurm")

    # job submission options
    parser.add_argument('--walltime', required=False, default='0-1:00:00', help='Time for job (default 1 hour; 0-1:00:00)')
    parser.add_argument('--cpus', required=False, default='1', help='CPUs for job (default1)')
    parser.add_argument('--memory', required=False, default='2048', help='Memory for job (default 2048)')

    parser.add_argument('--compute', required=False,default = 'massive', help='Compute to use')
    parser.add_argument('--partition', required=False, help='Partition to use')

    parser.add_argument("--input", nargs="+", required=True, help="List of assembly inputs")
    #parser.add_argument("--outdir", type=str, required=True, help="Directory for output")
    
    return parser.parse_args()

def main():

	# Get arguments
    args = parse_args()

    #if args.outdir[-1] != "/":
    #    args.outdir += "/"
    #if args.proteins == "":
    #    print ('No protein list provided, using default database')
    #if args.rundir == "":
    #    args.rundir = os.getcwd()

    for filepath in args.input:
        filepath_str = str(filepath)

        #get the tail end of the file path
        filename = str(os.path.basename(filepath))
        edited_filename = filename + "_edited.fasta"

        #read in fasta file and write new file, edited_filename which only has contigs >= 2bp long
        input_seq_iterator = SeqIO.parse(filepath,"fasta")
        output_seq_iterator = (record for record in input_seq_iterator if len(record.seq) >= 2)
        SeqIO.write(output_seq_iterator, edited_filename, "fasta")

        # Create job instance
        job_name =  '%s_executable' % filename
        job = job_scheduler.Slurm(job_name=job_name, time=args.walltime,
                                          cpus=args.cpus, memory_per_cpu=args.memory)

        # Add job command and modules
        job_command = "\nexport SINGULARITYENV_PREPEND_PATH=/opt/CRISPRCasFinder/bin"
        job_command += "\nmkdir " + filename + "_output"
        job_command += "\ncd " + filename + "_output"
        job_command += "\nCRISPRCasFinder.pl -so /opt/CRISPRCasFinder/sel392v2.so -levelMin 3 -cas --in ../" + edited_filename
        
        job.commands.append(job_command)
        job.modules.append(env_modules.get_module(args.compute, 'crispr'))


        # Submit job and write out SBATCH
        job_sbatch_fp = '%s_sbatch.txt' % job_name
        job.submit_job()
        job.write_submit_script(job_sbatch_fp)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
