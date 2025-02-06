+++
title: Genomic Comparison Metrics
published: 2025-02-06
description: Average Nucleotide Identity and Aligned Fraction are useful metrics for quantifying the similarity of genomes. This article will explain them.
image: https://images.unsplash.com/photo-1637929476734-bd7f5f78e40a
+++

# Genomic Comparison Metrics

Average Nucleotide Identity (ANI) and Aligned Fraction (AF) are useful metrics for quantifying the similarity of genomes. This article will explain them.

## Average Nucleotide Identity

This measure answers the question of "how similar are the two genomes". There are various ways to compute the ANI, since it relies on first performing a pairwise *alignment*, and there are many different alignment algorithms. Regardless, the formula is the same once you have aligned your genomes. 

```math
ANI = \frac{\sum_{i=1}^{N} I_i}{N}
```

Before we use this, we must

1. Obtain 2 genomes
2. Assemble both as best you can, ideally
3. Cut them up into fragment of `$N$` length (say 1000bp)
4. Try out best to align the fragments from genome A to fragments from genome B
5. Take the average all the aligned fragments above some threshold, completely ignoring unmatched fragments

Maybe we have 5 fragments:

| Fragment | Identity | Note |
|---|--------------|--|
| 1 | 98% | |
| 2 | 96% | |
| 3 | 80% | |
| 4 | 15% | Discard |
| 5 | 98% | |

Average is 93%, so the ANI is 93%.

## Alignment Fraction

ANI measures *aligned* sequence identity, it does have an obvious problem -- we just completed ignored the 4th fragment! Imagine if fragments 1, 2, 3 and 5 were 100% - it would give the illusion the genomes are identical, which isn't the case.

Alignment Fraction (AF) solves for this. It tells us *how much of the genomes aligned*.

```math
AF = \frac{\sum \text{Aligned Length}}{\text{Total Genome Length}}
```

This woulkd work out to 80% for the above example - 4 out of the 5 fragments aligned to a high enough percentage (based on whatever threshold we choose). We don't consider how much of the sequences aligned - just the number that did.
