+++
title: Gene Calling
published: 2025-02-24
description: I explain what gene calling is, and some of the specifics around doing so in viruses.
+++

# Gene Calling in Viruses

*Gene Calling* is a fancy way of saying "this region of DNA corresponds to a gene". This is usually done with computational models, using heuristics such as:

- open reading frames (ORFs)
- start / stop codons
- ribosome binding sites
- etc

Doing so in viruses is particularly tricky for many reasons, one of which is **overlapping ORFs**. For example, you might have a DNA strand:

```
AUG AAT AUG GAG ATG UGA UAA

AUG AAT AUG GAG ATG UGA
^^^                 ^^^
start               end 

**OR**

AUG AAT AUG GAG ATG UGA UAA
    ^^^                 ^^^
    start               end 
```

Both are valid ORFs, depending where transcription starts. Viruses pack a whole lot into their genome. They are very efficient.
