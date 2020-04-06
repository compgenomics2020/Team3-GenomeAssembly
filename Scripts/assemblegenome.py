#! usr/bin/env python3
##Final script for Genome Assembly Team

##Input incase of folder location:
import argparse
import subprocess
	
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--folderlocation", help = "Path for required reads") # Input csv file
args = parser.parse_args()

samples=subprocess.check_output("ls "+args.folderlocation+" | grep -o '^.*_' | uniq", shell=True, universal_newlines=True)
idlist=samples.split()

for id in idlist:
    subprocess.run("spades.py --plasmid --careful -o /home/projects/group-c/Team3-GenomeAssembly/plasmidSpades/"+id[:-1]+" --pe1-1 "+args.folderlocation+id+"r1.f* --pe1-2 "+args.folderlocation+id+"r2.f*", shell=True)


