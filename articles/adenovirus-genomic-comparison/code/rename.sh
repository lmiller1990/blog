#! /usr/bin/zsh

for dir in $(ls data); do
        find "data/$dir" -type f -name "*.fna" | while read -r fna_file; do
                echo "$fna_file -> $dir"
                sed -i "1s/.*/>$dir/" "$fna_file"
        done
done
