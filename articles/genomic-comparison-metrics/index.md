+++
title: Genomic Comparison Metrics
published: 2025-02-06
description: Average Nucleotide Identity and Aligned Fraction are useful metrics for quantifying the similarity of genomes. This article will explain them.
image: https://images.unsplash.com/photo-1637929476734-bd7f5f78e40a
+++

Average Nucleotide Identity (ANI) and Aligned Fraction (AF) are useful metrics for quantifying the similarity of genomes. This article will explain them.

## Average Nucleotide Identity

This measure answers the question of "how similar are the two genomes". There are various ways to compute the ANI, since it relies on first performing a pairwise *alignment*, and there are many different alignment algorithms. Regardless, the formula is the same once you have aligned your genomes. 

$$
\[
ANI = \frac{\sum_{i=1}^{N} I_i}{N}
\]

\[
ANI = \frac{I_1 + I_2 + \dots + I_N}{N}
\]
$$
