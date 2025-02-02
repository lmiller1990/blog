from Bio import AlignIO
from Bio.Align import AlignInfo

alignment = AlignIO.read("../aligned.aln", "clustal")

summary_align = AlignInfo.SummaryInfo(alignment)
consensus = summary_align.dumb_consensus()
print(consensus)
