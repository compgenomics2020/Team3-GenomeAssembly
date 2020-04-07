##Final script for Genome Assembly Team

import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data_directory', type = str, help = 'path to raw data')
parser.add_argument('--html', action='store_true', help = 'write html output')

args = parser.parse_args() 

################## QUALITY CONTROL

######### FASTP

# directories
fastp_dir = '/home/projects/group-c/Team3-GenomeAssembly/1.readQC/pipeline_temp'
trimmed_dir = '/home/projects/group-c/Team3-GenomeAssembly/2.trimmedReads/pipeline_temp'

# deleting previous directories, make new ones
subprocess.call(['rm', '-rf', fastp_dir, trimmed_dir])
subprocess.call(['mkdir', fastp_dir, trimmed_dir])

# assumptions about input files: all of the input files are contained in a single directory
# all of the files are .fq.gz files, samples have numerical ids
# read one: _1.fq.gz, read two: _2.fq.gz
for filename in os.listdir(args.data_directory):
    if filename.endswith('1.fq.gz'):
        id = filename[:-8]
        arg_list = ['fastp', 
        '-i', args.data_directory + '/' + id + '_1.fq.gz', 
        '-I', args.data_directory + '/' + id + '_2.fq.gz', 
        '-o', '{}/{}_r1.fq'.format(trimmed_dir, id),
        '-O', '{}/{}_r2.fq'.format(trimmed_dir, id),
        '-f', '5', '-F', '30', '-t', '10', '-e', '28', '-c', '-5', '5', '-M', '27',
        '-j', '{}/{}_fastp.json'.format(fastp_dir, id)] 

        if args.html == True:
            arg_list.append('-h')
            arg_list.append('{}/{}_fastp.html'.format(fastp_dir, id))
    subprocess.call(arg_list)

######### MULTIQC

# path to multiqc report: fastp_dir + multiqc_report.html
# '/home/projects/group-c/Team3-GenomeAssembly/1.readQC/pipeline_temp/multiqc_report.html'
subprocess.call(['multiqc', fastp_dir, '-o', fastp_dir])

################## ASSEMBLY

samples=subprocess.check_output("ls "+ trimmed_dir +" | grep -o '^.*_' | uniq", shell=True, universal_newlines=True)
idlist=samples.split()

######### PLASMIDSPADES

for id in idlist:
    subprocess.run("spades.py --plasmid --careful -o /home/projects/group-c/Team3-GenomeAssembly/plasmidSpades/"+id[:-1]+" --pe1-1 "+args.folderlocation+id+"r1.f* --pe1-2 "+args.folderlocation+id+"r2.f*", shell=True)
