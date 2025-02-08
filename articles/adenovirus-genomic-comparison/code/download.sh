#! /usr/bin/zsh
mkdir data

for g in {a,b,c,d,e,f,g}; do
        datasets download genome taxon "human mastadenovirus $g" --assembly-level complete --filename "hadv_$g.zip"
        mkdir "data/hadv_$g"
        unzip "hadv_$g.zip" -d "data/hadv_$g"
done

rm *.zip
