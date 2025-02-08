+++
title: Adenovirus Genomic Comparisons
published: 2025-02-06
description: TODO
image: https://images.unsplash.com/photo-1637929476734-bd7f5f78e40a
+++

# Adenovirus Genomic Comparisons: type F vs the world

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

Download the data:

```sh
#! /usr/bin/zsh
mkdir data

for g in {a,b,c,d,e,f,g}; do
        datasets download genome taxon "human mastadenovirus $g" --assembly-level complete --filename "hadv_$g.zip"
        mkdir "data/hadv_$g"
        unzip "hadv_$g.zip" -d "data/hadv_$g"
done

rm *.zip
```

In addition, rename the `fna` header to be a bit nicer:

```sh
#! /usr/bin/zsh

for dir in $(ls data); do
        find "data/$dir" -type f -name "*.fna" | while read -r fna_file; do
                echo "$fna_file -> $dir"
                sed -i "1s/.*/>$dir/" "$fna_file"
        done
done
```

## Running SKANI

Now we have some genomes, let's try it out. The default parameters are for larger genomes, so we need to tweak them:

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

Using the new `-c` flag:

```
skani dist -c 20 data/hadv_a/ncbi_dataset/data/GCA_000846805.1/GCA_000846805.1_ViralProj14517_genomic.fna data/hadv_a/ncbi_dataset/data/GCA_006415435.1/GCA_006415435.1_ASM641543v1_genomic.fna | cut -f3-
```

We get:

```
Align_fraction_ref    Align_fraction_query     Ref_name        Query_name

98.73   99.71   98.40   hadv_a  hadv_a
```

This is what we'd expect from two organisms supposedly closely related (same species).

How about the same comparison, but for the other types of Adenovirus?


```sh
#! /usr/bin/zsh

function average_ani {
        awk '{ sum1 += $3; sum2 += $4; count++ } 
        END { 
        if (count > 0) 
                print sum1 / count, sum2 / count 
        }'
}

for g in {a,b,c,d,e,f,g}; do
        files=("data/hadv_$g"/**/*.fna)

        # read ani1 ani2 < <(skani dist --small-genomes "${files[@]}" | average_ani)
        read ani1 ani2 < <(skani dist -c 20 "${files[@]}" | average_ani)
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
#!/usr/bin/zsh
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
    files_target=("data/hadv_$target"/**/*.fna)
    files_cousin=("data/hadv_$cousin"/**/*.fna)
    # NOTE we use -c 20
    read ani1 ani2 < <(skani dist -q "${files_target[@]}" -r "${files_cousin[@]}" -c 20 | average_ani)
    echo "ANI between Adenovirus $target and $cousin: $ani1, $ani2"
done
```

We get:

Comparing Adenovirus f to its cousins...

- ANI between Adenovirus F and A: 46.2533, 10.14
- ANI between Adenovirus F and B: 68.8725, 16.7455
- ANI between Adenovirus F and C: 0, 0
- ANI between Adenovirus F and D: 76.6281, 19.3789
- ANI between Adenovirus F and E: 74.2882, 20.9326
- ANI between Adenovirus F and F: 98.3608, 98.6093
- ANI between Adenovirus F and G: 76.4716, 24.8242

There are some variants that are closer to Adenovirus F, such as D, E and G, in terms of ANI. The AF is very far apart. I'm interested in identifying in metagenomic data, though, so the ANI is probably the more important metric to focus on. Ideally, we want to find some unique loci that are only found in Adenovirus F, and no other Adenoviruses, and ideally, no other organisms.

Adenovirus F is quite distinct from the other adenovirus species. We should be able to find some way to identify it uniquely within some genomic data.
