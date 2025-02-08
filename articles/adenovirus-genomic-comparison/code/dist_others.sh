#!/usr/bin/zsh
function average_ani {
        awk '{ sum1 += $3; sum2 += $4; count++ } 
        END { 
        if (count > 0) 
                print sum1 / count, sum2 / count 
        }'
}

target="f"
cousins=(a b c d e f g)

echo "Comparing Adenovirus $target to its cousins..."

for cousin in "${cousins[@]}"; do
    files_target=("data/hadv_$target"/**/*.fna)
    files_cousin=("data/hadv_$cousin"/**/*.fna)
    # NOTE we use -c 20
    read ani1 ani2 < <(skani dist -q "${files_target[@]}" -r "${files_cousin[@]}" -c 20 | average_ani)
    echo "ANI between Adenovirus $target and $cousin: $ani1, $ani2"
done
