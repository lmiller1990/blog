+++
title: A Simple ChIP Seq Pipeline
published: 2024-07-04
description: I recently finished my first semester of a Masters of Bioinformatics at UQ. BINF6000 exposed me to different types of bioinformatics workflows. In this post, I share one - an ChIP Seq pipeline - and discuss what each of the tools does.
image: https://images.unsplash.com/photo-1637929476734-bd7f5f78e40a
+++

# A Simple ChIP Seq Pipeline

I recently finished my first semester of a Masters of Bioinformatics at UQ. BINF6000 exposed me to different types of bioinformatics workflows. In this post, I share one - an ChIP Seq pipeline - and discuss what each of the tools does.

## Understanding the Data

I have a control dataset for Fruitfly (Drosophila). This means an ChIP Seq experiment was conducted without any enrichment or modification to the DNA.

```
data/control.fastq.gz
```

Let's peak inside! We can do that with `zless data/control.fastq.gz`

```
@K00242:156:HGLMKBBXX:3:1101:1692:1191 1:N:0:NAGTCA
NCCTCACTGTGGCGGTCACTTCAGCACTGAGAGAAAATGCGGATGAACCA
+
#AAFFJFFAJFJJFJJJJJJFJJJJJJF7JAJJJJFJJJJ-7FF<AJJJJ
```

This is what a `fastq` file looks like. It is one of the most common file formats you find in bioinformatics.

The format is:

1. Header line
2. Sequence line
3. Separator line
4. Quality line

Breaking it down:

## 1. Header line

As a reminder, this is the header line:

```
@K00242:156:HGLMKBBXX:3:1101:1692:1191 1:N:0:NAGTCA
```

The format:

```
@<instrument>:<run ID>:<flowcell ID>:<lane>:<tile>:<x-pos>:<y-pos>
```

- K00242: the machine, eg an Illumina sequencer.
- 156: Run id. Every time you use your Illumina machine, run id increases.
- HGLMKBBXX: "flow cell" id. This is the id of the cell where the DNA is loaded. I don't fully understand what a flow cell is, but it's a physical location in a machine somewhere.
- The remaining one are all related to the location within a flow cell. Not relevant for this pipeline.

## 2. The DNA Sequence

It's the sequence. A C G T and N for ambiguous.

## 3. Divider

Does nothing. It's basically just white space.

## 4. Quality

ASCII representation of the Phred score. This is a reflection of the quality of the data.

# Quality Control

Throughout any pipeline, you want to constantly perform quality control to ensure the data set is good, and that everything is proceeding as expected. One popular program for this is FastQC.

Let's see the quality of the data with `fastqc`:

```
fastqc data/control.fastq.gz
```

It generates a HTML report. Here's one of the failed metrics, at least according to FastQC out of the box:

![](https://github.com/lmiller1990/lachlan-miller.me/blob/master/app/public/static/chip-seq/Pasted%20image%2020240627130148.png?raw=true)
The blue line is the theoretically "perfect" distribution. This is not realistic - some organisms are far more GC than AT, for example. This one actually looks pretty good. Looking at the spike in the center - we see 1.8M reads are right around the 50% GC mean content mark.

The actual organism, Drosophila, has around 42% GC. There is a spike in that are in our graph. The major spike at 50% is kind of surprising - maybe there is some contamination, or perhaps the presence of the adapters is impacting it. 

Adapters are additional sequences added by the sequencing machine - we generally want to remove those before doing any sort of analysis, since they are not part of the actual biological dataset. Another report from FastQC about adapters:

![](https://github.com/lmiller1990/lachlan-miller.me/blob/master/app/public/static/chip-seq/Pasted%20image%2020240627131248.png?raw=true)
We can remove it with a program called `cutadapt`:

```
cutadapt -a AGATCGGAAGAGCACACGTCAGAACTCCAGTCACGAGTCAATCTCGTATG -o output.fastq data/control.fastq.gz
```

Let's check the quality again:

```
fastqc output.fastq
```

![](https://github.com/lmiller1990/lachlan-miller.me/blob/master/app/public/static/chip-seq/Pasted%20image%2020240629105741.png?raw=true)

Weird, right? The issue is after removing the adapters, we are left with a bunch of empty space. See below:

![[Screenshot 2024-06-29 at 10.58.34 AM.png]]

I found this surprising, but it is the expected result. It's even in the documentation:

> By default, empty reads are kept and will appear in the output. If you do not want this, use the `--minimum-length`/`-m` [filtering option](https://cutadapt.readthedocs.io/en/stable/guide.html#filtering).

We can filter them using `-m` for minimum. `$1` is your the input file.

```sh
adapter="AGATCGGAAGAGCACACGTCAGAACTCCAGTCACGAGTCAATCTCGTATG"
cutadapt -a $adapter -m 40 -o output.fastq $1
```

The empty, overrepresented sequences are gone. You can also see no reads with a length less than 40 are present.

![](https://github.com/lmiller1990/lachlan-miller.me/blob/master/app/public/static/chip-seq/Pasted%20image%2020240629112835.png?raw=true)

I did the same thing for my `treatment_rep1` file. After trimming some adapters:


```
cutadapt -a AGATCGGAAGAGCACACGTCAGAACTCCAGTCACGGAGAAATCTCGTATG -a AACACAACACAACACAACACAACACAACACAACACAACACAACACAACAC -o cleaned/treatment1_rep1.fastq.gz -m 40 data/treatment_rep1.fastq.gz
```

![](https://github.com/lmiller1990/lachlan-miller.me/blob/master/app/public/static/chip-seq/Pasted%20image%2020240701222847.png?raw=true)
# Read Mapping

We are now happy with our data set. Next is read mapping! Right now, we have a bunch of reads, mostly around 50 bp (base pairs), as the graph shows. We need to figure out where those map on the reference genome. So, we need

1. Reference genome. [Get it here](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000001215.4/)
2. Mapping tool. Let's use `bowtie2`, this one is popular and widely used.

Looking at the dataset:

```
└── data
    ├── GCA_000001215.4
    │   └── GCA_000001215.4_Release_6_plus_ISO1_MT_genomic.fna
    ├── GCF_000001215.4
    │   └── GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna
    ├── assembly_data_report.json
    ├── data_summary.tsv
    └── dataset_catalog.json
```

The two main files are:
- GCA_000001215.4
- GCF_000001215.4

Both are the same data, but in a different format.

- GCA is **Genome Component Archive**
- GCF is **Genome Reference Consortium**

The difference:

- **GCA** is a bigger database that anyone can submit to. There are duplicates, the data is pretty raw, and the quality is not guaranteed.
- **GCF** is the **RefSeq** database. It is carefully reviewed and curated. It aims to provide a single, standardized version for each entity.

So if you want more data, GCA is for you. If you want to focus on quality, GCF.

Now we have a reference, we need to do the alignment. But what is an alignment? 

An example alignment:

```
  Read:      GACTGGGCGATCTCGACTTCG
             |||||  |||||||||| |||
  Reference: GACTG--CGATCTCGACATCG
```

The reference genome has some gaps aded (shown by `-`). Genomes don't actually have gaps - what is more likely is some extra bases were *inserted* into the read, either via chance mutation, or perhaps the read is just wrong.

Here is how the reference looks:

```
>NC_004354.4 Drosophila melanogaster chromosome X
GAATTCGTCAGAAATGAgctaaacaaatttaaatcattaaatgcGAGCGGCGAATCCGGAAACAGCAACTTCAAACCAGT
```

It's really long:

```
wc -l genome/ncbi_dataset/data/GCF_000001215.4/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna
1799366 
```

I am not sure what the difference between the lower and upper case characters are. I asked ChatGPT:

- **Lowercase letters** often denote sequences that have been "soft-masked." Soft-masking, as a part of the sequence analysis and annotation process, usually indicates the presence of regions in the genome that are repetitive or less confident in terms of sequence integrity (e.g., high mutation rates areas or complex regions that are difficult to sequence accurately).
- **Uppercase letters** represent the regions of the genome with higher confidence in their sequence accuracy. These may likely be single-copy or non-repetitive regions more critical for gene coding and regulatory functions.

I suspect this is accurate - lower case means less confidence. I don't think it makes a difference for this experiment, anyway, but always good to scrutinize your data.

To use bowtie2, we also need to build an index. We can do it like this:

```
bowtie2-build <reference>.fa index/output
```

My exact command:

```
bowtie2-build genome/ncbi_dataset/data/GCF_000001215.4/GCF_000001215.4_Release_6_plus_ISO1_MT_genomic.fna index
```

This is what I got:

```
index.1.bt2	index.2.bt2	index.3.bt2	index.4.bt2	index.rev.1.bt2	index.rev.2.bt2
```

These are binary formats - not readable by humans. No problem, they are for bowtie, not for us!

Now, we do the alignment!

```
bowtie2 -x index/index. -U data/output.fastq > data/output.sam
```

Output:

```
9818 reads; of these:
  9818 (100.00%) were unpaired; of these:
    278 (2.83%) aligned 0 times
    8350 (85.05%) aligned exactly 1 time
    1190 (12.12%) aligned >1 times
97.17% overall alignment rate
```

Looking at the output, it is a SAM file. This stands for Sequence Alignment Map. First we have a bunch of lines that look like this:

```
@HD	VN:1.5	SO:unsorted	GO:query
@SQ	SN:NC_004354.4	LN:23542271
@SQ	SN:NW_001845990.1	LN:1625
```

The first line is the header. 
- VN is version. 
- SO is sorting order - ours is unsorted.
- GO is the grouping order - ours is by query. I do not know what this means.

SQ is a Sequence Dictionary.
- SN:... is a sequence name. This maps to a database, in our case, RefSeq.
- LN is the length. In this case, 23542271 bp long. That is 23m pairs! [This one points to the entire X chromosome](https://www.ncbi.nlm.nih.gov/nuccore/NC_004354).

After about 1500 SQ entries, we hit the data:

```
@SQ	SN:NW_007931121.1	LN:76973
@SQ	SN:NC_024511.2	LN:19524
@PG	ID:bowtie2	PN:bowtie2	VN:2.5.3	CL:"/opt/homebrew/bin/../Cellar/bowtie2/2.5.3/bin/bowtie2-align-s --wrapper basic-0 -x index/index -U data/output.fastq"
K00242:156:HGLMKBBXX:3:1224:28787:26687	16	NT_033777.3	21051814	42	50M	*	0	0	GTTTATGAACCGTTTTTGGTACGCTTTTCAATTAGAATTTAGTTATTGTG	JJJJJJJ<-JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJFFFAA	AS:i:0	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:50	YT:Z:UU
K00242:156:HGLMKBBXX:3:1221:22424:23048	0	NT_033778.4	20711542	42	50M	*	0	0	GCCCTTCCGCGCTCAAAAAGGATTTATTCTCGTGCTTAACTTGGCTTAGC	AAFFFJJJJJJJJJJJJJJJ7JJJJJJJJJJJJJJJJJJJJJJJJJJJJJ	AS:i:0	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:50	YT:Z:UU
K00242:156:HGLMKBBXX:3:1226:8775:48632	16	NT_033778.4	3199693	30	50M	*	0	0	AGCGAACCAATTAGTGATTGAAAATGGGTTATATTTACCTTTGCACATTT	JJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJFFAAA	AS:i:0	XS:i:-6	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:50	YT:Z:UU
```

PG is the program entry. It has information about what we used to generate this SAM file.

The rest of the file is the aligment records. This is what we came for. Each column, given
```
K00242:156:HGLMKBBXX:3:1226:8775:48632	16	NT_033778.4	3199693	30	50M	*	0	0	AGCGAACCAATTAGTGATTGAAAATGGGTTATATTTACCTTTGCACATTT	JJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJFFAAA	AS:i:0	XS:i:-6	XN:i:0	XM:i:0	XO:i:0	XG:i:0	NM:i:0	MD:Z:50	YT:Z:UU
```

- Read name: K00242:156:HGLMKBBXX:3:1226:8775:48632
	- This is the unique identifier. ID, flow cell ID, lane, all that stuff from the Illumina machine.
- Flag: 16
	- Additional info. 16 means mapped in reverse complement direction. I need to learn more to understand this.
- NT_033778.4
	- As discussed, an identifier. In this case, Drosophila melanogaster chromosome 2R, [see it here](https://www.ncbi.nlm.nih.gov/nuccore/NT_033778.4/)
- 3199693
	- This is where the alignment starts as. This is a position. This is around 3m in - the whole gencome is around 180m bp.
- 30
	- This is the quality (PHRED score)
- 50M
	- CIGAR string. This is how reads map to the reference. 50M means exactly 50 bases perfectly match!
- Some more columns, then ...
-  The actual read that was mapped.
```
AGCGAACCAATTAGTGATTGAAAATGGGTTATATTTACCTTTGCACATTT
```
- The phred score for each base.
```
JJJJJJJJJJJFJJJJJJJJJJJJJJJJJJJJJJFJJJJJJJJJJFFAAA
```

## More formats: SAM and BAM

SAM is human readable. It is a big file - many gigabytes, even for a simple fruitfly. Instead, we can use BAM - binary alignment mapping. We can pipe the stdout of `bowtie2` into `samtools` and write it straight to a BAM file.
```
bowtie2 -x reference/bowtie2_index/genome -U cleaned/treatment1_rep1.fastq.gz | samtools view -bS - > cleaned/treatment_rep1_aligned.bam
```

## Peek Calling

We are doing as [ChiP Seq](https://en.wikipedia.org/wiki/ChIP_sequencing) experiment. The goal is to identify which proteins TF (transcription factors) bind to. To do this, once we have generated our data, we use [peek calling](https://en.wikipedia.org/wiki/Peak_calling). If the initial experiment followed correct ChiP Seq protocols, there should be a lot more reads mapped to regions to which TFs bind. Peek calling identifies those peaks (a genomic region).

Here is an example of a peek:

![](https://github.com/lmiller1990/lachlan-miller.me/blob/master/app/public/static/chip-seq/Pasted%20image%2020240702205353.png?raw=true)

We want to identify the "peeks" - a genomic location with more reads than the rest. There are a bunch of programs, the most popular is MACS.

MACS has a lot of different functions. We want `callpeak`. The `macs3 callpeak --help` gives us a good command:

```
1. Peak calling for regular TF ChIP-seq:
    $ macs3 callpeak -t ChIP.bam -c Control.bam -f BAM -g hs -n test -B -q 0.01
2. Broad peak calling on Histone Mark ChIP-seq:
    $ macs3 callpeak -t ChIP.bam -c Control.bam --broad -g hs --broad-cutoff 0.1
3. Peak calling on ATAC-seq (paired-end mode):
    $ macs3 callpeak -f BAMPE -t ATAC.bam -g hs -n test -B -q 0.01
4. Peak calling on ATAC-seq ( focusing on insertion sites, and using single-end mode):
    $ macs3 callpeak -f BAM -t ATAC.bam -g hs -n test -B -q 0.01 --shift -50 --extension 100
```

We want the first one: 

```
macs3 callpeak -c <control> -t <treatment> -f BAM -g dm -n <label> -B -q 0.01
```

My command is:
```
macs3 callpeak -c cleaned/control_aligned.bam -t cleaned/treatment_rep1_aligned.bam -f BAM -g dm -n macs_output/dm -B -q 0.01
```

I passed `-n macs_output/dm` as the label, so that is where the output goes:

```
macs_output
├── dm_control_lambda.bdg
├── dm_model.r
├── dm_peaks.narrowPeak
├── dm_peaks.xls
├── dm_summits.bed
└── dm_treat_pileup.bdg
```

A bunch of files! `dm_peaks.narrowPeak` is what we are interested in. It is basically a BED file.

```
chr2L	16685	17074	macs_output/dm_peak_1	62	.	1.64721	8.09327 6.28438	71
```

The format:
- chr2L - the chromosome which the peak maps to
- 16685 - start coordinate
- 17074 - end coordinate
- macs_output/dm_peak_1 - this is a label
- score - value depends on what the tool documentation specifies.
- `-`. This is the "strand". I don't fully understand this.
- 1.64 is the fold enrichment. This describes how many more specific DNA sequences are bound by proteins in the ChIP sample than the control. A value of 1 implies no enrichment; great than 1 implies more DNA was bound in the treatment; biological significance.
- 8.09 - the p-value in -log(10). This means the peak is **statistically significant**. A value of 0 would represent not statistical significance.
- 6.28 - a q-value. Similar to a p-value. I am not sure about this or why it's useful. 

## What does this all mean?

We've got a bunch of peaks - genomic locations that proteins (TFs) bind to. The next thing is to see what genes are in those areas! We can do it programatically with some code, or using amino a genome viewer.

One popular viewer is the [USCS viewer](https://genome.ucsc.edu/). I find it hard to use and confusing. I used the igv.org viewer, it's more simple, at least for me, as a beginner.

I loaded the dm6 genome and my narrowPeak file:

![](https://github.com/lmiller1990/lachlan-miller.me/blob/master/app/public/static/chip-seq/Pasted%20image%2020240703215155.png?raw=true)

I searched for the gene that is in the center of the peak in the NCBI. [Here it is](https://www.ncbi.nlm.nih.gov/gene/33156/ortholog/?scope=6656 and landed here: https://www.ncbi.nlm.nih.gov/gene/33156/).

This region is "lethal (2) giant larvae".

> Enables several functions, including SNARE binding activity; myosin II binding activity; and protein kinase inhibitor activity.

This is outside my area of understanding. I looked up those terms:

- SNARE binding: Not sure, too much biology jargon.
- Myosin II: something to do with muscle contraction.
- Protein kinase inhibitor activity: Protein kinases are enzymes that modify other proteins chemically by adding a phosphate group which alters activity and function. Protein kinase inhibitor activity, therefore, is about preventing the phosphorylation.

# Conclusion and Next Steps

This post demonstrates how the create a simple ChIP Seq pipeline. Tools and file formats include:

- FastQC - quality control
- bowtie2 - read mapping
- MACS3 - peek calling
- samtools - for working with SAM files
- File formats: fastq, SAM, BAM

Some improvements would be:

- write in all together in a bash script, for easy of use
- use NextFlow or Snakemake to declare the steps for easily sharing and deploying in a platform agnostic fashion
- more exploration of the peeks, and how to decide which ones are of the most interest

