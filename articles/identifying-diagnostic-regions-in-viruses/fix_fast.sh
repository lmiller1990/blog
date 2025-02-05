#!/bin/bash

# Loop over all .fasta files in the current directory
for file in *.fasta; do
    # Use sed to add a space after '>' if there isn't one
    sed -i 's/^>\([^ ]\)/> \1/' "$file"
done
