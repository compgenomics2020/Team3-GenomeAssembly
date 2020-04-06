import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data_directory', type = str, help = 'path to raw data')

parser.add_argument('--html', action='store_true', help = 'write html output')

args = parser.parse_args() 

'''
-i and -I - supply paired-end input files
-o and -O - supply the path to the output for the trimmed fastq files
-f - number of bases to trim from front of mate 1
-F - number of bases to trim from front of mate 2
-t - number of bases to trim from end of both mates (can supply a -T argument to trim different numbers from both mates)
-e - average quality threshold; reads under this threshold will be discarded
-c - turns on paired-end base correction (has a small effect on quality at ends of mate 2)
-5 - turns on sliding window trimming from 5' end, only bases within the window that don't meet the threshold are discarded
-M - quality threshold for sliding window
-j - path to json QC report
'''

######### FASTP ARGS

for filename in os.listdir(args.data_directory):
    if filename.endswith('1.fq.gz'):
        id = filename[:-8]
        arg_list = ['fastp', 
        '-i', args.data_directory + '/' + id + '_1.fq.gz', 
        '-I', args.data_directory + '/' + id + '_2.fq.gz', 
        '-o', '{}/{}_r1.fq'.format('/home/projects/group-c/Team3-GenomeAssembly/2.trimmedReads/pipeline', id),
        '-O', '{}/{}_r2.fq'.format('/home/projects/group-c/Team3-GenomeAssembly/2.trimmedReads/pipeline', id),
        '-f', '5', '-F', '30', '-t', '10', '-e', '28', '-c', '-5', '3', '-M', '27',
        '-j', '{}/{}_fastp.json'.format('/home/projects/group-c/Team3-GenomeAssembly/1.readQC/pipeline', id)] 

        if args.html == True:
            arg_list.append('-h')
            arg_list.append('{}/{}_fastp.html'.format('/home/projects/group-c/Team3-GenomeAssembly/2.trimmedReads/pipeline', id))
    subprocess.call(arg_list)

'''
example query:
fastp -i CGT3002_1.fq -I CGT3002_2.fq 
-o trimmed/CGT3002_r1.fq -O trimmed/CGT3002_r2.fq 
-f 5 -F 30 -t 10 -e 28 -c -5 3 -M 27 
-j reports/CGT3002_fastp.json -h reports/CGT3002_fastp.html
'''
