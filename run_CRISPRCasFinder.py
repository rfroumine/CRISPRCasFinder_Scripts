#!/usr/bin/env python
#
# Submit multiple CRISPRCasFinder jobs to SLURM (input: assembly files)
#
# Authors - Roni Froumine, Kelly Wyres, Stephen Watts
#
# Last modified - Feb 25, 2019
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

    # get arguments
    args = parse_args()

    for filepath in args.input:
        filepath_str = str(filepath)

        # get base name of file path
        filename = str(os.path.basename(filepath))
        edited_filename = filename + "_edited.fasta"

        # read in fasta file and write new file with suffix 'edited.fasta' 
        # which only has contigs which are at least 2 bp long (requirement for CRISPRCasFinder)
        input_seq_iterator = SeqIO.parse(filepath,"fasta")
        output_seq_iterator = (record for record in input_seq_iterator if len(record.seq) >= 2)
        SeqIO.write(output_seq_iterator, edited_filename, "fasta")

        # Create job instance
        job_name =  '%s_executable' % filename
        job = job_scheduler.Slurm(job_name=job_name, time=args.walltime,
                                          cpus=args.cpus, memory_per_cpu=args.memory)

        # Add job command and modules
        
        #job_command = "\n#SBATCH --qos=shortq"

        job_command = "\nmodule load miniconda3/4.1.11-python3.5"
        job_command += "\nsource activate /projects/js66/software/conda_envs/crisprcasfinder"

        job_command += "\nmkdir " + filename + "_output"
        job_command += "\ncd " + filename + "_output"
        job_command += "\nCRISPRCasFinder.pl -so /projects/js66/software/conda_envs/crisprcasfinder/lib/vmatch/sel392.so -cas -minDR 19 -minSP 20 -levelMin 3 -def SubTyping --in ../" + edited_filename
        
        job.commands.append(job_command)

        # Submit job and write out SBATCH
        job_sbatch_fp = '%s_sbatch.txt' % job_name
        job.submit_job()
        job.write_submit_script(job_sbatch_fp)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
