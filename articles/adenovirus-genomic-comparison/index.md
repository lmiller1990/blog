+++
title: Adenovirus Genomic Comparisons
published: 2025-02-06
description: TODO
image: https://images.unsplash.com/photo-1637929476734-bd7f5f78e40a
+++

# ...

In this article we analyze various Adenovirus F genomes using the ANI (Average Nucleotide Identity) and AF (Aligned Fraction). I wrote more about those [here](/articles/genomic-comparison-metrics).

Now, I want to answer two questions:

1. How much variation is there between different Adenovirus F genomes? If we use the ANI, this would be the *intra* ANI.
2. How much variation is there between different Adenovirus F and other Adenoviruses?. If we use the ANI, this would be the *inter* ANI.

Starting with question 1, we need some Adenovirus F genomes. We can get some from the NCBI [Genome Assembly Database](https://www.ncbi.nlm.nih.gov/grc/data), using the `datasets` CLI tool.

```sh
datasets summary genome taxon "human mastadenovirus F" --assembly-level complete
```

We get a bunch of datasets:

```json
{
   "accession" : "GCA_006437595.1",
   "assembly_info" : {
      "assembly_level" : "Complete Genome",
      "assembly_method" : "Bowtie2 v. 2.1.0; Unipro UGENE v. 1.16.1",
      "assembly_name" : "ASM643759v1",
      "assembly_status" : "current",
      "assembly_type" : "haploid",
      "release_date" : "2016-03-21",
      "sequencing_tech" : "Illumina",
      "submitter" : "Institute of Molecular Life Sciences, University of Zurich"
   },
   "assembly_stats" : {
      "contig_l50" : 1,
      "contig_n50" : 34210,
      "gc_count" : "17532",
      "gc_percent" : 51,
      "number_of_component_sequences" : 1,
      "number_of_contigs" : 1,
      "number_of_scaffolds" : 1,
      "scaffold_l50" : 1,
      "scaffold_n50" : 34210,
      "total_number_of_chromosomes" : 1,
      "total_sequence_length" : "34210",
      "total_ungapped_length" : "34210"
   },
   "current_accession" : "GCA_006437595.1",
   "organism" : {
      "infraspecific_names" : {
         "strain" : "HoviX"
      },
      "organism_name" : "Human adenovirus 40",
      "tax_id" : 28284
   },
   "source_database" : "SOURCE_DATABASE_GENBANK"
}
```

Nice information, but we really need the nucleotide sequence if we are going to get the ANI and AF. In this case, we do not want `datasets summary ...` but `datasets download ...`. `summary` is useful to see what we will get, and then once we are happy, `download` will get the datasets.

## Running SKANI

Now we have some genomes, let's try it out:


```sh
skani dist GCA_000846685.1/GCA_000846685.1_ViralProj14487_genomic.fna GCA_006402115.1/GCA_006402115.1_ASM640211v1_genomic.fna
skani dist  GCA_000846685.1/GCA_000846685.1_ViralProj14487_genomic.fna GCA_006402115.1/GCA_006402115.1_ASM640211v1_genomic.fna | cut -f3-5 | ./md.sh
```


| ANI | Align_fraction_ref | Align_fraction_query |
| --- |  --- |  --- |
| 83.51 | 33.04 | 32.96 |

So, in this example, ANI is around 83% - lots of similar nucleotides, as expected. Compared to something like two human, though, this is very low! In the wild west of virus genomics, not so much. The AF is only 33% - this suggests *most* of the genomes were not aligned. This could be explain by:

- large divergence, even within the species
- lots of rearrangement / duplication / insertions
- Adenovirus F tend to be not that similar, despite all falling undre the Adenovirus F group.

ANI and AF can be tuned using some parameters. Out of the box, skani works well for larger genomes, like bacteria.

It turns out you can do

> *Since v0.2.2, skani has the --small-genomes option equivalent to -c 30 -m 200 --faster-small.*

`-c` and `-m` are as follows:

```
ALGORITHM PARAMETERS:
    -c <c>                   Compression factor (k-mer subsampling rate).       [default: 125]
        --faster-small       Filter genomes with < 20 marker k-mers more aggressively. Much faster
                             for many small genomes but may miss some comparisons.
    -m <marker_c>            Marker k-mer compression factor. Markers are used for filtering.
                             Consider decreasing to ~200-300 if working with small genomes (e.g.
                             plasmids or viruses).      [default: 1000]
```

Imagine a genome like a book you are scanning. A higher `-c` value would be like scanning for important words - good, fast, but you might miss details. A small `-c` would be like reading every word - more accurate but also much more computationally expensive.

For large genomes (bacteria, eukaryotes) using a low `-c` value is prohibitively expensive. For a virus, though, not so much!

Using the new `--small-genomes` flag:

```
| ANI | Align_fraction_ref | Align_fraction_query |
| --- |  --- |  --- |
| 89.30 | 89.55 | 89.35 |
```

We now see the AF is much higher. This is likely a more accurate representation, and what we'd expect from two organisms supposedly closely related (same species).

How about the same comparison, but for the other types of Adenovirus?

First, we need some genomes:

```
for i in {a,b,c,d,e,f,g}; do
        datasets download genome taxon "human mastadenovirus $i" --assembly-level complete --filename "human_mastadenovirus_$i.zip"
        echo "Got human-mastadenovirus_$i.zip"
        du -h "human_mastadenovirus_$i.zip"
done
```

Unzip them

```
for zip in human_mastadenovirus_*; do 
        OUT=$(echo $zip | cut -d '.' -f 1); unzip $zip -d $OUT; 
done
```

Now, run the same comparison:

```sh
#!/bin/bash
shopt -s globstar  # Enable recursive globbing in Bash

function average_ani {
        awk '{ sum1 += $3; sum2 += $4; count++ } 
        END { 
        if (count > 0) 
                print sum1 / count, sum2 / count 
        }'
}

for g in {a,b,c,d,e,f,g}; do
        files=(human_mastadenovirus_"$g"/**/*.fna)

        read ani1 ani2 < <(skani dist --small-genomes "${files[@]}" | average_ani)
        echo "Adenovirus $g ANI / AF: $ani1, $ani2"
done
```

Mostly what you'd expect:

```
Adenovirus A ANI / AF: 88.7894, 92.0555
Adenovirus B ANI / AF: 89.3602, 91.8232
Adenovirus C ANI / AF: 96.886, 94.7767
Adenovirus D ANI / AF: 96.1763, 98.8405
Adenovirus E ANI / AF: 94.1114, 95.3837
Adenovirus F ANI / AF: 89.541, 89.4118
Adenovirus G ANI / AF: 90.3919, 90.0256
```

## Adenovirus F vs Others

Now we can do the same thing, but see how Adenovirus F compares to the rest, one by one, using `-q` (query) and `-r` (reference):

```sh
target="f"
cousins=(a b c d e f g)

echo "Comparing Adenovirus $target to its cousins..."

for cousin in "${cousins[@]}"; do
    files_target=(human_mastadenovirus_"$target"/**/*.fna)
    files_cousin=(human_mastadenovirus_"$cousin"/**/*.fna)

    # Ensure both sets of files exist before running skani
    read ani1 ani2 < <(skani dist --small-genomes "${files_target[@]}" "${files_cousin[@]}" | average_ani)
    echo "ANI between Adenovirus $target and $cousin: $ani1, $ani2"
done
```

We get:

Comparing Adenovirus f to its cousins...

- ANI between Adenovirus f and a: 0, 0
- ANI between Adenovirus f and b: 0, 0
- ANI between Adenovirus f and c: 0, 0
- ANI between Adenovirus f and d: 0, 0
- ANI between Adenovirus f and e: 0, 0
- ANI between Adenovirus f and f: 98.196, 98.3431
- ANI between Adenovirus f and g: 0, 0

Everything except the identity comparison is 0. This suggests each Adenovirus group has very little in common, as per the skani docs:

> If the resulting aligned fraction for the two genomes is < 15%, no output is given.
>
> In practice, this means that only results with > ~82% ANI are reliably output (with default parameters). See the skani advanced usage guide for information on how to compare lower ANI genomes.

I looked into advanced usage, it recommends lowering `-c` and `-s`.

```
-c <c> Compression factor (k-mer subsampling rate).       
        [default: 125]
-s <s> Screen out pairs with *approximately* < % identity using k-mer sketching. 
        [default: 80]
```

## What do these mean?

`-s` is the screening ANI threshold. This means skani will only proceed if "kmer similarity estimate" is **greater than** `-s`. Default is 80: only genomes with >=80% similarity are compared. So, we might need this to be lower to be more lenient.

- if `-s` too high: miss genomes that are pretty similar
- if `-s` too low: get poor matches that aren't similar
I tried a few different numbers. Eventually, `-c 20` seems better.

`-c` is the kmer compression factor. Default is 125. Imagine you are comparing two songs. `-c` controls how many notes you listen to before deciding if the songs are similar.

- if -c is high (eg: 200), you listen to only a few key notes (faster, but risk missing differences).
- if -c is low (eg: 30), you listen to every note (slower but more detailed comparison)

Updated parameters:

```sh
#!/bin/bash
shopt -s globstar  # Enable recursive globbing in Bash

function average_ani {
        awk '{ sum1 += $3; sum2 += $4; count++ } 
        END { 
        if (count > 0) 
                print sum1 / count, sum2 / count 
        }'
}

target="f"
cousins=(a b c d e f g)

echo "Comparing Adenovirus $target to its cousins..."

for cousin in "${cousins[@]}"; do
    files_target=(human_mastadenovirus_"$target"/**/*.fna)
    files_cousin=(human_mastadenovirus_"$cousin"/**/*.fna)
    # NOTE we use -c 20
    read ani1 ani2 < <(skani dist -q "${files_target[@]}" -r "${files_cousin[@]}" -c 20 | average_ani)
    echo "ANI between Adenovirus $target and $cousin: $ani1, $ani2"
done
```

Now we get:

Comparing Adenovirus f to its cousins...

- ANI between Adenovirus f and a: 46.2533, 10.14
- ANI between Adenovirus f and b: 68.8725, 16.7455
- ANI between Adenovirus f and c: 0, 0
- ANI between Adenovirus f and d: 76.6281, 19.3789
- ANI between Adenovirus f and e: 74.2882, 20.9326
- ANI between Adenovirus f and f: 98.3608, 98.6093
- ANI between Adenovirus f and g: 76.4716, 24.8242

There are some variants that are closer to Adenovirus F, such as D, E and G, in terms of ANI. The AF is very far apart. I'm interested in identitying in metagenomic data, though, so the ANI is probably the more important metric to focus on. Ideally, we want to find some unique loci that are only found in Adenovirus F, and no other Adenoviruses, and ideally, no other organisms.

## General Comparison

We can use skani's `triangle` function to calculate the distance from "the rest". `dist` vs `triangle` can be described like this:

- How different is Adenovirus F from a SPECIFIC group? → Use skani dist (we did this)
- How different is Adenovirus F from ALL other adenoviruses? → Use skani triangle (now)

To show what triangle does, here is an example running `triangle` against 1 genome from each group:


```
#!/usr/bin/zsh

# select one representative genome per Adenovirus group
declare -A representatives

for group in {a,b,c,d,e,f,g}; do
    # Find the first .fna file in the group directory
    genome_file=(human_mastadenovirus_"$group"/**/*.fna(om[1]))
    representatives[$group]="$genome_file"
done

# run skani triangle only on the selected genomes
skani triangle -c 15 -s 40 --min-af 5 "${representatives[@]}" -o adenovirus_ani_matrix.txt
```

This gives us:

```
7
human_mastadenovirus_a
human_mastadenovirus_b  0.00
human_mastadenovirus_c  0.00	0.00
human_mastadenovirus_d	0.00	0.00	0.00
human_mastadenovirus_e	0.00	85.13	0.00	0.00
human_mastadenovirus_f	0.00	0.00	0.00	0.00	0.00
human_mastadenovirus_g	0.00	0.00	0.00	0.00	0.00	0.00
```

This shows the ANI for each pair. So the first 0.00 is the ANI when comparing `human_mastadenovirus_b` and `human_mastadenovirus_a`. Only one entry is non-zero - B and E.

We can confirm this using `dist`

```sh
$ skani dist -c 15 -s 40 human_mastadenovirus_b/.../GCA_006446875.1_ASM644687v1_genomic.fna human_mastadenovirus_e/.../GCA_023119645.1_ASM2311964v1_genomic.fna
ANI     Align_fraction_ref
85.13   78.19
```

`skani triangle` is basically a way to do a lot of `skani dist` all at once.

Before we go further, let's update the `fna` files to have a more readable header. We will show the Adenovirus group in the header:

```sh
#! /usr/bin/zsh

for dir in $(ls); do
        echo $i
        find "$dir" -type f -name "*.fna" | while read -r fna_file; do
                echo "$fna_file -> $dir"
                sed -i "1s/.*/>$dir/" "$fna_file"
        done
done
```

I ran `triangle` on the 3 genomes from each group:

```sh
21
human_mastadenovirus_a
human_mastadenovirus_a	99.98
human_mastadenovirus_a	99.54	99.60
human_mastadenovirus_b	0.00	0.00	0.00
human_mastadenovirus_b	0.00	0.00	0.00	0.00
human_mastadenovirus_b	0.00	0.00	0.00	0.00	99.39
human_mastadenovirus_c	0.00	0.00	0.00	0.00	0.00	0.00
human_mastadenovirus_c	0.00	0.00	0.00	0.00	0.00	0.00	99.62
human_mastadenovirus_c	0.00	0.00	0.00	0.00	0.00	0.00	97.66	97.59
human_mastadenovirus_d	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00
human_mastadenovirus_d	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	97.10
human_mastadenovirus_d	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	93.65	93.90
human_mastadenovirus_e	0.00	0.00	0.00	83.17	0.00	0.00	0.00	0.00	0.00	82.22	81.92	81.16
human_mastadenovirus_e	0.00	0.00	0.00	83.21	0.00	0.00	0.00	0.00	0.00	82.18	81.88	81.11	99.87
human_mastadenovirus_e	0.00	0.00	0.00	84.69	0.00	0.00	0.00	0.00	0.00	83.01	82.54	0.00	96.29	96.32
human_mastadenovirus_f	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00
human_mastadenovirus_f	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	99.93
human_mastadenovirus_f	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	99.81	99.79
human_mastadenovirus_g	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00
human_mastadenovirus_g	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00
human_mastadenovirus_g	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	0.00	92.35	99.18
```

Looks like B and E might have something in common... but it's still mostly 0s. I ran `triangle` on the entire dataset - all 0s. I think we can reasonly deduce that Adenoviruses are fairly different from each other.
