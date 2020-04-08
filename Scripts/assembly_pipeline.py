##Final script for Genome Assembly Team

import glob
import subprocess
import argparse

""" parser = argparse.ArgumentParser()
parser.add_argument('data_directory', type = str, help = 'path to raw data')
parser.add_argument('--html', action='store_true', help = 'write html output')

args = parser.parse_args()  """

################## QUALITY CONTROL

######### FASTP

# directories
raw_dir = '/home/projects/group-c/data'
fastp_dir = '/home/projects/group-c/Team3-GenomeAssembly/1.readQC/pipeline_temp'
trimmed_dir = '/home/projects/group-c/Team3-GenomeAssembly/2.trimmedReads/pipeline_temp'
assembly_dir = '/home/projects/group-c/Team3-GenomeAssembly/3.Spades/pipeline_temp'
passembly_dir = '/home/projects/group-c/Team3-GenomeAssembly/4.plasmidSpades/pipeline_temp'
quality_dir = '/home/projects/group-c/Team3-GenomeAssembly/5.Assemblyquality/pipeline_temp'

# assumptions about input files: all of the input files are contained in a single directory
# all of the files fit the pattern *.f*, both of the reads for the sample share a sample id
# read one: _1.f*, read two: _2.f*

# load fastq files into fastp
def run_fastp(raw_dir, fastp_dir, trimmed_dir, html = False):

    # deleting previous directories, make new ones
    subprocess.call(['rm', '-rf', fastp_dir, trimmed_dir])
    subprocess.call(['mkdir', fastp_dir, trimmed_dir])

    for filename in glob.glob(raw_dir + '/*1.f*'):
        id = filename[len(raw_dir):filename.find('.') - 2]
        arg_list = ['fastp', 
            '-i', filename, 
            '-I', glob.glob('{}*{}*2*'.format(raw_dir, id))[0],
            '-o', '{}/{}_r1.fq'.format(trimmed_dir, id),
            '-O', '{}/{}_r2.fq'.format(trimmed_dir, id),
            '-f', '5', '-F', '30', '-t', '10', '-e', '28', '-c', '-5', '5', '-M', '27',
            '-j', '{}/{}_fastp.json'.format(fastp_dir, id)] 

            # if you want html reports for each sample, we can do that. but why would we?
        if html == True:
            arg_list.append('-h')
            arg_list.append('{}/{}_fastp.html'.format(fastp_dir, id))
        subprocess.call(arg_list)

######### MULTIQC

# output: multiqc report, fastp_dir + 'multiqc_report.html'
# '/home/projects/group-c/Team3-GenomeAssembly/1.readQC/pipeline_temp/multiqc_report.html'
def run_multiqc(fastp_dir):
    subprocess.call(['multiqc', fastp_dir, '-o', fastp_dir])

################## GENOME ASSEMBLY





################## PLASMID ASSEMBLY

def run_plasmidspades(trimmed_dir, passembly_dir):
    samples = subprocess.check_output("ls "+ trimmed_dir +" | grep -o '^.*_' | uniq", shell=True, universal_newlines=True)
    idlist = samples.split()

    for id in idlist:
        # delete previous temporary directories, make new temporary directories
        id_dir = passembly_dir + '/' + id[:-1]
        subprocess.call(['rm', '-rf', id_dir])
        subprocess.call(['mkdir', id_dir])

        # run plasmid spades
        subprocess.call(['spades.py', '--plasmid', '--careful', '-o', id_dir, '--pe1-1', '{}/{}r1.fq'.format(trimmed_dir, id), '--pe1-2', '{}/{}r2.fq'.format(trimmed_dir, id)])


################## ASSEMBLY QUALITY

def run_assemblyquality(assembly_dir,quality_dir):
    idlist = subprocess.check_output("ls "+assembly_dir, shell = True, universal_newlines = True)
    subprocess.call(['rm', '-rf', quality_dir, '/assemblyfiles'])
    subprocess.call(['mkdir',quality_dir, '/assemblyfiles'])
    subprocess.call(['rm', '-rf',quality_dir, '/quast'])
    subprocess.call(['mkdir',quality_dir, '/quast'])
    subprocess.call(['rm', '-rf',quality_dir, '/Busco'])
    subprocess.call(['mkdir',quality_dir, '/Busco'])

    for id in idlist:
        subprocess.call('cp '+assembly_dir+'/'+id+'/contigs.fasta '+quality_dir+'/assemblyfiles/'+id+'_contigs.fasta', shell = True, universal_newlines=True)
        subprocess.call(['rm', '-rf',quality_dir, '/Busco/', id])
        subprocess.call(['mkdir',quality_dir, '/Busco/',id])
        subprocess.call('busco -m Genome -i '+assembly_dir+'/'+id+' -l bacteria_odb10 -o '+quality_dir+'/Busco/'+id, shell = True, universal_newlines=True)    

    subprocess.call('quast '+qualitydir+'/assemblyfiles/* -o '+quality_dir+'/quast/ --circos', shell=True, universal_newlines=True)
    

def main():
    run_fastp(raw_dir, fastp_dir, trimmed_dir)
    run_multiqc(fastp_dir)
    run_plasmidspades(trimmed_dir, assembly_dir)
    run_assemblyquality(assembly_dir, quality_dir)

main()
