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
