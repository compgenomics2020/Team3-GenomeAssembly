# Team 3 Genome Assembly

This is a pipeline for assembling *Listeria monocytogenes* genomes. 

## Usage

```
python assembly_pipeline.py -i /home/projects/group-c/data -a SPADES
```
```
-a: --assembler. Choose the assembler to use: SPADES or SKESA. Default SPADES.
-i: --input_data_directory. Path to raw data.
--html: Output HTML reports in fastp.
```

The assembly_pipeline.py script takes in a single parameter, data_directory, which is a path to the raw fastq data. We assume that the input directory contains files that fit the pattern `*.f*`. We further assume that the read 1 and read 2 files for each sample start with the same sample ID, and the read 1 files end with `*1.f*` and the read 2 files end with `*2.f*`. 

## Quality Control and Trimming

* Fastp (v 0.20.0)
* MultiQC (v 1.8)

### Quality Control

Fastp is a tool that combines both quality control and trimming into a single, rapidly-implemented step, increasing the speed and usability of our pipeline. Since we had 50 input files in our pipeline, we used MultiQC to consolidate the 50 separate quality control reports generated by fastp into a single report.

The output of the quality control step of the pipeline is a PDF report generated by MultiQC that displays the quality of all of the samples run through the pipeline. 

### Trimming Parameters

The following arguments were supplied to fastp in order to trim our data: `-f 5 -F 30 -t 10 -e 28 -c -5 3 -M 27`.

* -f 5 - globally trims 5 bases from 5' end of mate 1
* -F 30 - globally trims 30 bases from 5' end of mate 2
* -t 10 - globally trims 10 bases from 3' end of both mates
* -e 28 - discards reads with an average quality score under 28
* -c - turns on paired-end base correction, which slightly increased the quality of the 3' end of mate 2
* -5 5 - turns on sliding window trimming from 5' end with a window size of 5
* -M 27 - sets a quality threshold of 27 for sliding window

## Genome Assembly

SPAdes (v3.13.0)
* -careful - tries to reduce the number of mismatches and short indels

SKESA (v2.3.0)
Uses default setting.

### Tools Benchmarked

|Tools   | version  |
|--------|----------| 
|Abyss   |  2.2.4   |
|MaSuRCA |  3.3.5   |
|SPAdes  |  3.14.0  |
|SKESA   |  2.3.0   |
|*StriDe*|  v.1.0   | 

*optional*

## Assembly Quality

Quast (v5.0.2)

BUSCO (v3.0.2)

## Authors

Deepali Kundnani

Aparna Maddala

Swetha Gowri Singu

Yiqiong Xiao

Ruize Yang



