import numpy as np
from collections import Counter
from Bio import AlignIO


def shannon_entropy(column):
    counts = Counter(column)
    freq = np.array(list(counts.values())) / sum(counts.values())
    return -np.sum(freq * np.log2(freq))


# alignment = AlignIO.read("../aligned.aln", "clustal")
alignment = AlignIO.read("../LC.aln", "clustal")
entropies = [shannon_entropy(column) for column in zip(*alignment)]

import matplotlib.pyplot as plt

plt.plot(entropies)
plt.xlabel("Genome Pos")
plt.ylabel("Shannon entropy")
plt.title("Genomic Variability in Adenovirus")
plt.show()
