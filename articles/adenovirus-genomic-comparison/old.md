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
